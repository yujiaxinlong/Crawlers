# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YousuuItem(scrapy.Item):
    userId = scrapy.Field()
    bookId = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    relativeRating = scrapy.Field()
    booklistNum = scrapy.Field()
#     description = scrapy.Field()
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
