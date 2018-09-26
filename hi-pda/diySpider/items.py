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

class PetItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    likeNum = scrapy.Field()
    wantPetNum = scrapy.Field()
    price = scrapy.Field()
    xueming = scrapy.Field()
    bieming = scrapy.Field()
    fenbuquyu = scrapy.Field()
    tixing = scrapy.Field()
    yuanchandi = scrapy.Field()
    shengao = scrapy.Field()
    weight = scrapy.Field()
    lifeTime = scrapy.Field()
    nianren = scrapy.Field()
    xijiao = scrapy.Field()
    youshan = scrapy.Field()
    diaomao = scrapy.Field()
    meirong = scrapy.Field()
    tiwei = scrapy.Field()
    koushui = scrapy.Field()
    xunlian = scrapy.Field()
    huoyue = scrapy.Field()
    chengshi = scrapy.Field()
    naihan = scrapy.Field()
    naire = scrapy.Field()
    yundong = scrapy.Field()
    descs = scrapy.Field()
    image_articles = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class PetArticleItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()