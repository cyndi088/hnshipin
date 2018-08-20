# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from .. items import ShopsItem


class HnspSpider(scrapy.Spider):
    name = 'hnsp'
    allowed_domains = ['www.hnshipin.com/l_dj/index.php?']
    start_urls = ['http://www.hnshipin.com/l_dj/index.php?page=1']

    def parse(self, response):
        resp = response.xpath("//div[@class='title']/text()").extract_first()
        shop_nums = self.get_num(resp)
        url = response.url
        current_page = self.get_page(url)
        next_page = current_page + 1
        next_url = 'http://www.hnshipin.com/l_dj/index.php?page=%d'
        url_prefix = 'http://www.hnshipin.com/l_dj/'
        href_list = response.xpath("//div[@class='fwlist']//a[@target='_blank']/@href").extract()
        for href in href_list:
            item = {}
            item['shop_id'] = self.get_num(href)
            rest_url = url_prefix + href
            request = Request(rest_url, callback=self.shop_parse, meta=item, dont_filter=True)
            yield request
        if current_page * 20 <= shop_nums:
            request = Request(next_url % next_page, callback=self.parse, dont_filter=True)
            yield request

    def shop_parse(self, response):
        meta = response.meta
        shop = ShopsItem()
        shop['id'] = meta['shop_id']
        shop['name'] = response.xpath("//div[@class='xx_box']//div[@class='title']/text()").extract_first()
        shop['address'] = response.xpath("//div[@class='xx_box']//div[@class='line'][2]/text()").extract_first()
        shop['cook_style'] = response.xpath("//div[@class='xx_box']//div[@class='line'][3]//div[1]/text()")\
            .extract_first()
        shop['area'] = response.xpath("//div[@class='xx_box']//div[@class='line'][3]//div[2]/text()").extract_first()
        shop['category'] = response.xpath("//div[@class='xx_box']//div[@class='line'][4]//div[1]/text()")\
            .extract_first()
        shop['take_out'] = response.xpath("//div[@class='xx_box']//div[@class='line'][4]//div[2]/text()")\
            .extract_first()
        shop['phone'] = response.xpath("//div[@class='xx_box']//div[@class='line'][5]//div[1]/text()")\
            .extract_first()
        images_url = response.xpath("//div[@class='leftimg']/img[@id='xqimg']/@src").extract_first()
        yield shop

    @staticmethod
    def get_page(url):
        res = re.findall('page=(\d+)', url)
        page = int(res[0])
        return page

    @staticmethod
    def get_num(st):
        res = re.findall('(\d+)', st)
        num = int(res[0])
        return num
