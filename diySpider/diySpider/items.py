# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiyItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    backgroundImg = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    article = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)



class PetCategory(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)