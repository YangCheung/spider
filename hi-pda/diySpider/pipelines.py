# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from diySpider.items import ThreadItem
import pymysql as pq
import os

class DiyspiderPipeline(object):
    def __init__(self):
        self.conn = pq.connect(host='localhost', user='root',
                               passwd='123456', db='bistu', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, ThreadItem):
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