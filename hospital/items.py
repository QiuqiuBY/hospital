# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #医院名称
    hospitalName = scrapy.Field()
    #医院等级
    hospitalGrade = scrapy.Field()
    #医院类型
    hospitalType = scrapy.Field()
    #省
    province = scrapy.Field()
    #市
    city = scrapy.Field()
    #区/县
    direct = scrapy.Field()
    #床位数
    bedNum = scrapy.Field()
    #医院地址
    address = scrapy.Field()

    pass
