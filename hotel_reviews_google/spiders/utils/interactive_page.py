import logging

from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def scroll_hotels_list(page: Page, hotels_per_page: int, n_th: int):
    "Scroll down hotels list"
    if n_th % hotels_per_page == (hotels_per_page - 1):
        try:
            await page.locator('xpath=//div[contains(@aria-label,\
"Resultados")]').hover()
            await page.mouse.wheel(0, 5*n_th*1000)
            await page.locator('xpath=//div[contains(@aria-label,\
"Resultados")]').press("End", timeout=10 * 1000)
            await page.locator(
                'xpath=//div[contains(@aria-label, "Resultado")]\
//a[contains(@class,"hfpxzc")]').nth(n_th).wait_for(timeout=10 * 1000)
            logging.info('Scroll - hotels list!!!!')
        except PlaywrightTimeoutError:
            logging.info('End - hotels list!!!!')


async def access_button_reviews(page: Page):
    try:
        await page.locator(
            'xpath=//button[contains(@aria-label, "Avaliações")]').wait_for(
                timeout=10 * 1000)
        await page.locator(
            'xpath=//button[contains(@aria-label, "Avaliações")]').click(
                timeout=10 * 1000)

    except PlaywrightTimeoutError:
        await page.locator(
            'xpath=//div[contains(@jsaction, "Reviews")]'
        ).wait_for(timeout=10 * 1000)
        await page.locator(
            'xpath=//div[contains(@jsaction, "Reviews")]'
        ).click(timeout=10 * 1000)


async def access_hotel(page: Page, n_th: int):
    await page.locator('xpath=//div[contains(@aria-label, "Resultado")]\
//a[contains(@class,"hfpxzc")]').nth(n_th).click(timeout=10 * 1000)


async def get_url_reviews_hotel(page: Page, n_th: int):
    url_hotels_review = await page.locator('xpath=//div[contains(@aria-label, \
"Resultado")]//a[contains(@class,"hfpxzc")]').nth(
        n_th).get_attribute('href')
    return url_hotels_review


async def count_reviews_before_scrolling(page: Page):
    prev_count_reviews = await page.locator('//div[contains\
(@class, "m6QErb")]/div/div[contains(@jsaction,"review.out")]').count()
    # import ipdb
    # ipdb.set_trace()
    return prev_count_reviews


async def count_reviews_after_scrolling(page: Page):
    current_count_reviews = await page.locator('//div[contains\
(@class, "m6QErb")]/div/div[contains(@jsaction,"review.out")]').count()
    return current_count_reviews


async def scroll_reviews_list(page: Page):
    await page.locator('xpath=//div[contains(@tabindex,"-1")]\
[contains(@jslog,"mutable:true")]').press("End")


async def break_by_reviews_count(
        prev_count_reviews: int, current_count_reviews: int,
        vars_output_hotel: dict
):
    if prev_count_reviews == current_count_reviews:
        print(f"Here {current_count_reviews} -\
{vars_output_hotel.get('hotel_name')}")
        raise PlaywrightTimeoutError("Empty output reviews")


async def break_by_reviews_scroll_element(
        page: Page, detect_scroll_element_reviews_list: str
):
    await page.locator(
        f'xpath={detect_scroll_element_reviews_list}')\
        .wait_for(timeout=5 * 1000)
    await page.locator(
        f'xpath={detect_scroll_element_reviews_list}')\
        .is_enabled(timeout=5 * 1000)


async def waiting_time(prev_count: int):
    seconds = (prev_count / 100) + 5
    return seconds
