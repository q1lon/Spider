# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals

import csv
import json
import codecs
import os
import sys


class FeirenzaiPipeline(object):
    tem = []
    out_tem = []
    key_tem = {}

    def process_item(self, item, spider):
        self.tem.append(dict(item))
        return item

    # def close_spider(self, spider):
        # print (spider.name)
        # for i in self.tem:
            # i['rank'] = int(float(i['rank']))
            # self.out_tem.append(i)
        # 按照大类分开存放

        # result = sorted(self.out_tem, key=lambda x: (x['rank']))
        # fp = codecs.open('output.txt', 'a+', 'utf-8')
        # fp.write(json.dumps(result, ensure_ascii=False) + "\n")
        # fp.close()
