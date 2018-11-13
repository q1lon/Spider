#!usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from feirenzai.items import FeirenzaiItem  # 引入item

import scrapy
import json
import codecs

class feirenzai(scrapy.Spider):
    name = 'feirenzai'
    start_urls = ['http://www.kuaikanmanhua.com/web/topic/531/']

    def parse(self, response):
        mingyan = response.css('tr')
        # tem = []
        # 实例化item类
        test_tem = []
        # test_tem.append(mingyan[0])
        # test_tem.append(mingyan[2])
        # print(test_tem)
        for v in mingyan:
            item = FeirenzaiItem()
            img = v.css('td')[0].css('a img::attr(src)').extract_first()  # 获取缩略图
            details = v.css('td')[0].css('a::attr(href)').extract_first()  # 详情页地址
            name = v.css('td')[1].css('a::attr(title)').extract_first()  # 题目名称
            num = v.css('td')[2].css('td::text').extract()[1].splitlines()[1].strip()  # 关注人数
            date = v.css('td')[3].css('td::text').extract_first()  # 发布日期
            detail_url = 'http://www.kuaikanmanhua.com' + details
            item['name'] = name
            item['img'] = img
            item['num'] = num,
            item['date'] = date,
            item['detail_url'] = detail_url,
            # item={
            #     'name':name,
            #     'img':img,
            #     'num':num,
            #     'date':date,
            #     'detail_url':detail_url
            # }

            # print(detail_url)
            request = scrapy.Request(url=detail_url, callback=self.parse_detail, dont_filter=True)
            request.meta['data'] = item
            yield request

        # next_page = response.css('li.next a::attr(href)').extract_first()  # css选择器提取下一页链接

        # if next_page is not None:  # 判断是否存在下一页
        # next_page = response.urljoin(next_page)

        # yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['data']
        item['detail_img'] = response.css('div.list').css('img::attr(data-kksrc)').extract()
        yield item
