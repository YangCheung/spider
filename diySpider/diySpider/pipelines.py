# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from diySpider.items import DiyItem
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
