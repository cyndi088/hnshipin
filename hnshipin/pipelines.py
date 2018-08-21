# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
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


class PicPhotoPeoplePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        重写ImagesPipeline类的file_path方法
        实现：下载下来的图片命名是以校验码来命名的，该方法实现保持原有图片命名
        return: 图片路径
        """
        image_guid = request.url.split('?')[0].split('/')[-1]  # 取原url的图片命名
        return 'facade/%s' % image_guid

    def get_media_requests(self, item, info):
        """
        遍历image_urls里的每一个url，调用调度器和下载器，下载图片
        return: Request对象
        图片下载完毕后，处理结果会以二元组的方式返回给item_completed()函数
        """
        try:
            for image_url in item['image_urls']:
                yield Request(image_url)
        except KeyError as e:
            pass

    def item_completed(self, results, item, info):
        """
        将图片的本地路径赋值给item['image_paths']
        param results:下载结果，二元组定义如下：(success, image_info_or_failure)。
        第一个元素表示图片是否下载成功；第二个元素是一个字典。
        如果success=true，image_info_or_error词典包含以下键值对。失败则包含一些出错信息。
         字典内包含* url：原始URL * path：本地存储路径 * checksum：校验码
        param item:
        param info:
        return:
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")  # 如果没有路径则抛出异常
        item['image_paths'] = image_paths
        return item
