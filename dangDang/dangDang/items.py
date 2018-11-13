# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class BookspiderItem(scrapy.Item):
    rank = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()
    price = scrapy.Field()
    comments = scrapy.Field()
    big_name = scrapy.Field()
    big_id = scrapy.Field()
    small_name = scrapy.Field()
    small_id = scrapy.Field()
    pass
