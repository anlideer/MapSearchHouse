# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    area = scrapy.Field()
    direction = scrapy.Field()
    rooms = scrapy.Field()
    photo = scrapy.Field()
    price = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    lnglat = scrapy.Field()