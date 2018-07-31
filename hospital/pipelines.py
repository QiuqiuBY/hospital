# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HospitalPipeline(object):

    def process_item(self, item, spider):
        #连接数据库
        self.conn = pymysql.connect(
            host='127.0.0.1', user='root', password="123456",
            database='pachong', port=3306, charset='utf8'
        )
        #创建游标
        self.cur = self.conn.cursor()

        sql = "INSERT INTO hospital(hospitalName,hospitalGrade,hospitalType,province,city,direct,bedNum,address) " \
              "values (%r,%r,%r,%r,%r,%r,%r,%r)" \
              %(item['hospitalName'],item['hospitalGrade'],item['hospitalType'],
                item['province'],item['city'] ,item['direct'],item['bedNum'],item['address'])
        #执行sql语句
        self.cur.execute(sql)
        #提交数据
        self.conn.commit()

        #关闭连接
        self.cur.close()
        self.conn.close()

        return item

