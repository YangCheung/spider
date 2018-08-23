# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from diySpider.items import DiyItem, PetItem, PetArticleItem
import os
import leancloud

leanId = os.environ["leanId"]
leanKey = os.environ["leanKey"]
leancloud.init(leanId, leanKey)

class DiyspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DiyItem):
            Content = leancloud.Object.extend("Diy")
            query = Content.query.equal_to("url", item["url"])
            try:
                query.first()
            except leancloud.errors.LeanCloudError as e:
                content = Content()
                content.set("category", item["category"])
                content.set("url", item["url"])
                content.set("backgroundImg", item["backgroundImg"])
                content.set("title", item["title"])
                content.set("desc", item["desc"])
                content.set("article", item["article"])
                content.save()

        return item

class PetArticlePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PetArticleItem):
            PetArticle = leancloud.Object.extend("PetArticle")
            where = PetArticle.query.not_equal_to('url', item["url"])
            content = PetArticle()
            content.set("content", item["content"])
            content.set("url", item["url"])
            try:
                content.save()
            except leancloud.errors.LeanCloudError as e:
                pass
        return item

class PetspiderPipeline(object):
    def process_item(self, item, spider):
        print("===== PetItem xxxx ======")
        if isinstance(item, PetItem):
            print("===== PetItem======")
            Content = leancloud.Object.extend("Pet")
            # query = Content.query.equal_to("url", item["url"])
            where = Content.query.not_equal_to('url', item["url"])
            content = Content()
            content.set('category', item['category'])
            content.set('url', item['url'])
            content.set('cover', item['cover'])
            content.set('name', item['name'])
            content.set('images', item['images'])
            content.set('likeNum', item['likeNum'])
            content.set('wantPetNum', item['wantPetNum'])
            content.set('price', item['price'])
            content.set('xueming', item['xueming'])
            content.set('bieming', item['bieming'])
            content.set('fenbuquyu', item['fenbuquyu'])
            content.set('tixing', item['tixing'])
            content.set('yuanchandi', item['yuanchandi'])
            content.set('lifeTime', item['lifeTime'])
            content.set('shengao', item['shengao'])
            content.set('weight', item['weight'])
            content.set('nianren', item['nianren'])
            content.set('xijiao', item['xijiao'])
            content.set('youshan', item['youshan'])
            content.set('diaomao', item['diaomao'])
            content.set('tiwei', item['tiwei'])
            content.set('koushui', item['koushui'])
            content.set('xunlian', item['xunlian'])
            content.set('huoyue', item['huoyue'])
            content.set('chengshi', item['chengshi'])
            content.set('naihan', item['naihan'])
            content.set('naire', item['naire'])
            content.set('yundong', item['yundong'])
            content.set('descs', item['descs'])
            content.set('image_articles', item['image_articles'])
            try:
                # query.first()
                content.save()
            except leancloud.errors.LeanCloudError as e:
                pass
        return item
