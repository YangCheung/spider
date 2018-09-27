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
        self.conn = pq.connect(host='localhost', user='root', passwd='123456', db='hipda', charset='utf8mb4')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, ThreadItem):            
            tid = item.get("tid", "N/A")
            title = item.get("title", "N/A")
            turl = item.get("turl", "N/A")
            with_img_attach = item.get("with_img_attach", "N/A")
            with_file_attach = item.get("with_file_attach", "N/A")
            tag = item.get("tag", "N/A")
            author_uid = item.get("author_uid", "N/A")
            author_username = item.get("author_username", "N/A")
            publish_date = item.get("publish_date", "")
            follow_post_count = item.get("follow_post_count", "N/A")
            read_count = item.get("read_count", "N/A")
            last_post_username = item.get("last_post_username", "N/A")
            last_post_date = item.get("last_post_date", "N/A")

            sql_query_tid = "select tid from f_geek where f_geek.tid = %s "
            self.cur.execute(sql_query_tid, tid)
            result = self.cur.fetchone()
            if result:
                sql_update_tid = "UPDATE f_geek SET with_img_attach = %s, with_file_attach = %s, follow_post_count = %s, read_count = %s, last_post_username = %s, last_post_date = %s  WHERE tid = %s "
                self.cur.execute(sql_update_tid, (with_img_attach, with_file_attach, follow_post_count, read_count, last_post_username, last_post_date ))
            else:                
                sql = ("insert into f_geek (tid, title, turl, with_img_attach, with_file_attach, tag, author_uid, author_username, publish_date, follow_post_count, read_count, last_post_username, last_post_date)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                self.cur.execute(sql, (tid, title, turl, with_img_attach, with_file_attach, tag, author_uid, author_username, publish_date, follow_post_count, read_count, last_post_date))
            self.conn.commit()
        return item