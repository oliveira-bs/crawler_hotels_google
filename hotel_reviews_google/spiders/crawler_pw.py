import asyncio
import itertools
import logging
import os
import sys
from typing import Iterable

import pendulum
import scrapy
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from scrapy.http import Request

from .utils.api_output_response import (parse_api_hotel, parse_api_review,
                                        response_parse_api_hotel,
                                        response_parse_api_reviews)
from .utils.custom_settings import crawl_settings
from .utils.interactive_page import (access_button_reviews, access_hotel,
                                     break_by_reviews_count,
                                     break_by_reviews_scroll_element,
                                     count_reviews_after_scrolling,
                                     count_reviews_before_scrolling,
                                     get_url_reviews_hotel, scroll_hotels_list,
                                     scroll_reviews_list, waiting_time)
from .utils.items import GoogleHotelPrices, GoogleHotels, GoogleHotelsReviews

today = pendulum.now().strftime("%Y%m%d")
basepath = os.path.dirname(__file__)
sys.path.append(basepath)


class HRGoogleSpider(scrapy.Spider):
    name = 'hotel_reviews_google'
    allowed_domains = ['google.com.br']
    homepage = '.'.join(['https://www', allowed_domains[0]])
    custom_settings = crawl_settings(
        bot_name=name, today=today, basepath=basepath)
    start_urls = ['https://www.google.com.br/maps']
    target_hotel_region = "Centro, Vassouras, Rio de janeiro, Brasil"
    # target_hotel_region = "penedo, itatiaia, rio de janeiro, Brasil"
    reviews_per_page = 9
    hotels_per_page = 6
    urls_reviews_api = []
    urls_hotels_api = []

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'playwright': True,
                                       'playwright_include_page': True,
                                       'errback': self.errback})

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.wait_for_load_state('load')
        await asyncio.sleep(3)
        await page.locator('xpath=//input[contains(@id, "searchbox")]').fill(
            self.target_hotel_region)
        # "penedo, itatiaia, rio de janeiro, Brasil")

        await asyncio.sleep(5)
        await page.locator('xpath=//input[contains(@id, "searchbox")]').press(
            "Enter")
        await asyncio.sleep(5)
        await page.locator('xpath=//button[contains(@aria-label,"Hot")]\
[@jsaction]').click(timeout=10 * 1000)

        """Access reviews in hotel item"""
        while True:
            try:
                for n_th in itertools.count(start=0, step=1):
                    await scroll_hotels_list(
                        page=page, hotels_per_page=self.hotels_per_page,
                        n_th=n_th)

                    await access_hotel(page=page, n_th=n_th)

                    url_reviews_hotel = await get_url_reviews_hotel(page=page,
                                                                    n_th=n_th)

                    prev_count_hotel = await page.locator('xpath=//div\
[contains(@aria-label, "Resultado")]//a[contains(@class,"hfpxzc")]').count()

                    seconds = await waiting_time(
                        prev_count=prev_count_hotel)

                    "get hotel json via API"
                    page.on('response',
                            lambda response:
                            parse_api_hotel(
                                response,
                                urls_hotels_api=self.urls_hotels_api))

                    await asyncio.sleep(seconds)

                    (dict_hotel_output,
                     vars_output_hotel,
                     hotel_prices) = response_parse_api_hotel()

                    logging.info(
                        f"Get Info - {vars_output_hotel.get('hotel_name')}")

                    output_hotels = GoogleHotels(
                        id=dict_hotel_output.get('id'),
                        name=dict_hotel_output.get('name'),
                        address=dict_hotel_output.get('address'),
                        city_province=dict_hotel_output.get('city_province'),
                        zip_code=dict_hotel_output.get('zip_code'),
                        type=dict_hotel_output.get('type'),
                        longitude=dict_hotel_output.get('longitude'),
                        latitude=dict_hotel_output.get('latitude'),
                        phone=dict_hotel_output.get('phone'),
                        link=dict_hotel_output.get('link'),
                        datetime=pendulum.now().strftime(
                            "%Y-%m-%d %H:%M:%S"),
                    )
                    yield output_hotels

                    logging.info(
                        f"Get Price - {vars_output_hotel.get('hotel_name')}")

                    for price in hotel_prices:
                        output_price = GoogleHotelPrices(
                            hotel_id=price.get('hotel_id'),
                            hotel_name=price.get('hotel_name'),
                            service_name=price.get('service_name'),
                            price=price.get('price'),
                            service_id=price.get('service_id'),
                            datetime=pendulum.now().strftime(
                                "%Y-%m-%d %H:%M:%S"),
                        )
                        yield output_price

                    yield scrapy.Request(
                        url=url_reviews_hotel,
                        callback=self.parse_review,
                        cb_kwargs=dict(
                            vars_output_hotel=vars_output_hotel),
                        meta={'playwright': True,
                              'playwright_include_page': True,
                              'errback': self.errback}
                    )

            except PlaywrightTimeoutError as e:
                logging.warning(f'Scrolling error in hotel list \n{e}')
                await page.close()
                break

    async def parse_review(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.wait_for_load_state('load')

        vars_output_hotel = kwargs.get('vars_output_hotel')

        await asyncio.sleep(5)
        await access_button_reviews(page=page)

        logging.info(f"Reviews Access - {vars_output_hotel.get('hotel_name')}")
        while True:
            try:
                prev_count_reviews = await count_reviews_before_scrolling(
                    page=page)

                seconds = await waiting_time(
                    prev_count=prev_count_reviews)

                if prev_count_reviews == 0:
                    await scroll_reviews_list(page=page)

                while True:
                    page.on('response',
                            lambda response:
                            parse_api_review(
                                response,
                                urls_reviews_api=self.urls_reviews_api)
                            )
                    await asyncio.sleep(seconds)

                    output_reviews = response_parse_api_reviews()

                    if output_reviews is not None:
                        break

                for review in output_reviews:
                    review.update(vars_output_hotel)

                    hotel_reviews = GoogleHotelsReviews(
                        id=review.get('id'),
                        review_age=review.get('review_age'),
                        hotel_id=review.get('hotel_id'),
                        hotel_name=review.get('hotel_name'),
                        score=review.get('score'),
                        language=review.get('language'),
                        type_trip=review.get('type_trip'),
                        group_trip=review.get('group_trip'),
                        room_rating=review.get('room_rating'),
                        service_rating=review.get(
                            'service_rating'),
                        location_rating=review.get(
                            'location_rating'),
                        guest_reviews=review.get(
                            'guest_reviews'),
                        guest_photos=review.get(
                            'guest_photos'),
                        highlights_hotel=review.get(
                            'highlights_hotel'),
                        source=review.get('source'),
                        datetime=pendulum.now().strftime(
                            "%Y-%m-%d %H:%M:%S"),
                        positive_review=review.get(
                            'positive_review'),
                        negative_review=review.get(
                            'negative_review'),
                    )
                    yield hotel_reviews

                await scroll_reviews_list(page=page)

                current_count_reviews = await count_reviews_after_scrolling(
                    page=page)

                await break_by_reviews_count(
                    prev_count_reviews=prev_count_reviews,
                    current_count_reviews=current_count_reviews,
                    vars_output_hotel=vars_output_hotel)

                detect_scroll_element_reviews_list = '//div\
[contains(@class, "lXJj5c")]/div[contains(@class, "qjESne")]'

                await break_by_reviews_scroll_element(
                    page=page, detect_scroll_element_reviews_list=detect_scroll_element_reviews_list)

            except PlaywrightTimeoutError:
                logging.info(f"End Reviews - \
{current_count_reviews} - {vars_output_hotel.get('hotel_name')}!!!!")
                self.urls_reviews_api.clear()
                await page.close()
                break

    async def errback(self, response, failure):
        page = failure.request.meta["playwright_page"]
        logging.error(f'*****\nError Page:\n{page.url}\n*****')
        await page.close()
