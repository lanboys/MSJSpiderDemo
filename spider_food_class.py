# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2

from lxml import etree

import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


def loadFoodClass1(url):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    foodClass = content.xpath('//div[@class="nav"]/ul/li[2]/div/div/div/dl')
    for item in foodClass:
        class1 = item.xpath("dt/a")
        if len(class1) > 0:
            text = class1[0].text
            href = class1[0].attrib.get("href")

            sql = "insert into lb_food_class ( name , level , url ) values ( %s, %s, %s)"
            params = (text, 1, href)
            print(sql % params)
            MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodClass2(url, parentId):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    foodClass = content.xpath('//div[@class="main"]/div/div/dl')
    print(foodClass)
    for item in foodClass:
        class1 = item.xpath("dt/a")
        if len(class1) > 0:
             text = class1[0].text
             href = class1[0].attrib.get("href")

             sql = "insert into lb_food_class ( name , parent_id , level , url ) values ( %s, %s, %s, %s)"
             params = (text, parentId, 2, href)
             print(sql % params)
             # MysqlHelper.MysqlHelper().cud(sql, params)


class FoodClass:

    def __init__(self, name, parentId, level, url):
        self.name = name
        self.parentId = parentId
        self.level = level
        self.url = url


if __name__ == "__main__":
    # loadFoodClass1("https://www.meishij.net/jiankang/")

    sql = "select url, id  from lb_food_class where level = %s"
    params = (1,)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    # for row in rows:
    #     print (row[0])
    #     loadFoodClass2(row[0])

    loadFoodClass2(rows[0][0], rows[0][1])
