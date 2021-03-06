# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + "..."
            return item
        else:
            return DropItem("Missing Text")



# class MongoPipleline(object):
#
#     def __init__(self,mongo_uri,mongo_db):
#         self.mongo_uri= mongo_uri;
#         self.mongo_db=mongo_db;
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         return cls(
#             mongo_uri = crawler.settings.get('MONGO_URL'),  #从setings中获取url setings:MONGO_RUL='localhost'
#             mongo_db = crawler.settings.get('MONGO_DB','items')     #从setings中获取db setings:MONGO_DB = 'quotes'
#         )
#
#     def open_sider(self,spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def process_item(self,item,spider):
#         name = item.__class__.__name__
#         self.db[name].insert(dict(item))
#         return item
#
#     def close_spider(self,spider):
#         self.client.close()

class MongoPipleline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['quotestutorial']

    def process_item(self,item,spider):
        self.db['quotes'].insert(dict(item))  # 字典形式
        return item

    def close_spider(self):
        self.client.close()