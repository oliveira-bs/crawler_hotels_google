# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleHotelsReviews(scrapy.Item):
    id = scrapy.Field()
    review_age = scrapy.Field()
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    score = scrapy.Field()
    language = scrapy.Field()
    type_trip = scrapy.Field()
    group_trip = scrapy.Field()
    room_rating = scrapy.Field()
    service_rating = scrapy.Field()
    location_rating = scrapy.Field()
    guest_reviews = scrapy.Field()
    guest_photos = scrapy.Field()
    highlights_hotel = scrapy.Field()
    source = scrapy.Field()
    datetime = scrapy.Field()
    positive_review = scrapy.Field()
    negative_review = scrapy.Field()


class GoogleHotels(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    city_province = scrapy.Field()
    zip_code = scrapy.Field()
    type = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    phone = scrapy.Field()
    link = scrapy.Field()
    datetime = scrapy.Field()


class GoogleHotelPrices(scrapy.Item):
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    service_name = scrapy.Field()
    price = scrapy.Field()
    service_id = scrapy.Field()
    datetime = scrapy.Field()
