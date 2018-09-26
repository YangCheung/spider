import pymongo

from diySpider.items import DiyItem, PetItem, PetArticleItem
import os


class PetMongoPipe(object):

    collection_name = 'pet_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = os.environ["mongo_uri"]
        self.mongo_db = mongo_db

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, PetItem):
            self.db[self.collection_name].insert_one(dict(item))
        else:
            return item