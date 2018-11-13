# -*- coding: utf-8 -*
from __future__ import absolute_import
from __future__ import unicode_literals
import scrapy
import requests
from scrapy.selector import Selector
from dangDang.items import BookspiderItem
from lxml import etree

#dangdang.com 图书销量排行
class bookSpider(scrapy.Spider):
    name = 'bookBestsellers'
    # start_urls = ['http://bang.dangdang.com/books/bestsellers/01.21.02.00.00.00-recent7-0-0-1-%d'%i for i in range(1,5)]
    # start_urls = []

    allowed_domains = ["dangdang.com"]
    start_urls = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                              Safari/537.36 SE 2.X MetaSr 1.0'

    def start_requests(self):
        headers = {'User-Agent': self.user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)

    # 获取大分类
    def parse(self, response):
        headers = {'User-Agent': self.user_agent}
        lists = response.body.decode('gbk')
        selector = etree.HTML(lists)
        category_big_list = selector.xpath('//*[@id="sortRanking"]//*[@class="side_nav"]')

        for category_big in category_big_list:
            try:
                category_big_name = category_big.xpath('a/text()').pop()  # text
                category_big_url = category_big.xpath('a/@href').pop()  # href
                category_big_id = category_big.xpath('@category_path').pop()  # id
                # print (category_big_name, category_big_url, category_big_id)
                # category_big_url = "http://category.dangdang.com/pg1-cp01.{}.00.00.00.00.html". \
                #     format(str(category_big_id))
                yield scrapy.Request(url=category_big_url, headers=headers, callback=self.detail_parse,
                                     meta={"big_id": category_big_id, "big_name": category_big_name})
            except Exception:
                pass

    # 获取小分类
    def detail_parse(self, response):
        contents = etree.HTML(response.body.decode('gbk'))
        category_small_list = contents.xpath('//*[@id="sortRanking"]/ul[@class="side_nav_detail"]/li')

        for category_small in category_small_list:
            try:
                category_small_name = category_small.xpath('a/text()').pop()
                category_small_url = category_small.xpath('a/@href').pop()
                small_id = category_small_url.split('-')[0]
                small_id = small_id.split('/')[-1]
                # print (category_small_name, category_small_url, small_id)
                # category_small_url = "http://category.dangdang.com/pg1-cp01.{}.{}.00.00.00.html".\
                #                   format(str(response.meta["ID1"]),str(category_small_id))
                headers = {'User-Agent': self.user_agent}

                yield scrapy.Request(url=category_small_url, headers=headers, callback=self.third_parse,
                                     meta={"big_id": response.meta["big_id"],
                                           "big_name": response.meta["big_name"], "small_id": small_id,
                                           "small_name": category_small_name})
            except Exception:
                pass

    # 获取小分类下的排行数据 前100
    def third_parse(self, response):
        for i in range(1, 6):
            url = 'http://bang.dangdang.com/books/bestsellers/' + response.meta["small_id"] + '-24hours-0-0-1-%d' % i
            print(url)
            headers = {'User-Agent': self.user_agent}
            yield scrapy.Request(url=url, headers=headers, callback=self.ret_parse,
                                 meta={"big_id": response.meta["big_id"],
                                       "big_name": response.meta["big_name"], "small_id": response.meta["small_id"],
                                       "small_name": response.meta["small_name"]})
    # 获取小分类下的排行数据
    def ret_parse(self, response):

        item = BookspiderItem()
        sel = Selector(response)
        book_list = response.css('ul.bang_list.clearfix.bang_list_mode').xpath('li')

        for book in book_list:
            rank = book.css('div.list_num').xpath('text()').extract_first()
            print (rank)
            item['rank'] = rank
            item['name'] = book.css('div.name').xpath('a/text()').extract_first()
            item['author'] = book.css('div.publisher_info')[0].xpath('a/text()').extract_first()
            item['press'] = book.css('div.publisher_info')[1].xpath('a/text()').extract_first()
            item['price'] = book.css('span.price_n').xpath('text()').extract_first()
            item['comments'] = book.css('div.star').xpath('a/text()').extract_first()
            item['comments'] = book.css('div.star').xpath('a/text()').extract_first()
            item['small_id'] = response.meta["small_id"]
            item['small_name'] = response.meta["small_name"]
            item['big_id'] = response.meta["big_id"]
            item['big_name'] = response.meta["big_name"]
            yield item
