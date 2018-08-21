# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HnshipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ShopsItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    cook_style = scrapy.Field()
    area = scrapy.Field()
    category = scrapy.Field()
    take_out = scrapy.Field()
    phone = scrapy.Field()
    photo_path = scrapy.Field()


class PicPhotoPeopleItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    # 存放url的下载地址
    image_urls = scrapy.Field()
    # 图片下载路径、url和校验码等信息（图片全部下载完成后将信息保存在images中）
    images = scrapy.Field()
    # 图片的本地保存地址
    image_paths = scrapy.Field()