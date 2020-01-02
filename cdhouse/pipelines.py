# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem
import pymongo

class CdhousePipeline(object):

    collection_name = 'cdhome'
    
    def __init__(self, mongo_uri, mongo_db,mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.batch_list = []
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'cdhouse'),
            mongo_port=crawler.settings.get('MONGO_port')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        url:str = item['url']
        if url.find("search") > 0:
            raise DropItem("inValid item found: %s" % item)
        else:
            if len(self.batch_list) < 30:
                self.batch_list.append(dict(item))
            else:
                self.db[self.collection_name].insert_many(self.batch_list)
                self.batch_list.clear()
            return item
