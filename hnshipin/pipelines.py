# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from datetime import datetime


class HnshipinPipeline(object):
    def process_item(self, item, spider):
        return item


class MongodbPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_user, mongo_psw, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_psw = mongo_psw
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawlder):
        return cls(
            mongo_host=crawlder.settings.get('MONGO_HOST'),
            mongo_port=crawlder.settings.get('MONGO_PORT'),
            mongo_user=crawlder.settings.get('MONGO_USER'),
            mongo_psw=crawlder.settings.get('MONGO_PSW'),
            mongo_db=crawlder.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        cls = item.__class__.__name__
        if cls == 'ShopsItem':
            item['address'] = self.drop_colon(item['address'])
            item['cook_style'] = self.drop_colon(item['cook_style'])
            item['area'] = self.drop_colon(item['area'])
            item['category'] = self.drop_colon(item['category'])
            item['take_out'] = self.drop_colon(item['take_out'])
            item['phone'] = self.drop_colon(item['phone'])
            self.save_shops(item)
        return item

    def save_shops(self, item):
        # self.db['shops'].save(dict(item))
        self.db['shops'].find_one_and_update({'_id': item['id']},
                                             {'$set': {'data': item, 'update_time': datetime.now()}},
                                             upsert=True)

    @staticmethod
    def drop_colon(st):
        resp = st.split('：')
        need_st = resp[1]
        return need_st