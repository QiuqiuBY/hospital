# -*- coding: utf-8 -*-
import scrapy

from hospital.items import HospitalItem
from urllib.parse import urlencode


class MyhospitalSpider(scrapy.Spider):
    name = 'myhospital'
    allowed_domains = ['db.yaozh.com']
    start_urls = ['https://db.yaozh.com/hmap?&pageSize=30']

    def parse(self, response):
        #省份列表
        provinceList = ['北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省',
                        '江西省', '山东省', '河南省', '湖北省', '湖南省',
                        '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '内蒙古', '广西', '西藏', '宁夏', '新疆']
        #构建每一个省份的url
        for province in provinceList:
            print(province)
            data = {'province': province}
            pro = urlencode(data)
            proUrl = 'https://db.yaozh.com/hmap?&pageSize=30&{}'.format(pro)
            #传递url给下一个函数
            request = scrapy.Request(url=proUrl, callback=self.getUrl)
            request.meta['url'] = proUrl
            # print(proUrl)
            yield request

    def getUrl(self, response):
        #由不同省份url中获取的网页源代码
        page = response.xpath('//div[@class="tr offset-top"]/@data-max-page').extract()[0]
        page = int(page)
        #构建翻页的url
        for i in range(1, page):
            proUrl = response.meta['url'] + '&{}'
            data = {'p': str(i)}
            page = urlencode(data)
            pageUrl = proUrl.format(page)
            #传递翻页url给获取详情的函数
            request = scrapy.Request(url=pageUrl, callback=self.getInfo)
            request.meta['page_url'] = pageUrl
            # print(pageUrl)
            yield request

    def getInfo(self, response):
        #根据不同省份的不同页数的网页源代码，刷选出所需信息
        hospitalList = response.xpath('//table[@class="table table-striped"]/tbody/tr')
        # 储存对象
        item = HospitalItem()

        for hospital in hospitalList:
            # 医院名称
            hospitalName = hospital.xpath('./th/a/text()').extract()[0]
            # 医院等级
            hospitalGrade = hospital.xpath('./td[1]/text()').extract()
            if len(hospitalGrade) != 0:
                hospitalGrade = hospitalGrade[0]
            else:
                hospitalGrade = '未定级'
            # 医院类型
            hospitalType = hospital.xpath('./td[2]/text()').extract()[0]
            # 省
            province = hospital.xpath('./td[3]/text()').extract()[0]
            # 市
            city = hospital.xpath('./td[4]/text()').extract()[0]
            # 区/县
            direct = hospital.xpath('./td[5]/text()').extract()[0]
            # 床位数
            bedNum = hospital.xpath('./td[6]/text()').extract()
            if len(bedNum) != 0:
                bedNum = bedNum[0]
            else:
                bedNum = 0
            # 医院地址
            address = hospital.xpath('./td[7]/text()').extract()[0]

            print(hospitalName, hospitalGrade, hospitalType, province, city, direct, bedNum, address)
            #信息保存并传递给管道
            item['hospitalName'] = hospitalName
            item['hospitalGrade'] = hospitalGrade
            item['hospitalType'] = hospitalType
            item['province'] = province
            item['city'] = city
            item['direct'] = direct
            item['bedNum'] = bedNum
            item['address'] = address

            yield item
