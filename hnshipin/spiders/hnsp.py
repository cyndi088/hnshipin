# -*- coding: utf-8 -*-
import scrapy


class HnspSpider(scrapy.Spider):
    name = 'hnsp'
    allowed_domains = ['www.hnshipin.com/l_dj/index.php?']
    start_urls = ['http://www.hnshipin.com/l_dj/index.php?/']

    def parse(self, response):
        pass
