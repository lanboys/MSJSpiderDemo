# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import sys
import time
import urllib2

from lxml import etree

import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')


def loadFoodClass1():
    """
        爬取第一分类
    """
    url = "https://www.meishij.net/jiankang/"
    content = getContent(url)
    dlList = content.xpath('//div[@class="nav"]/ul/li[2]/div/div/div/dl')

    for dl in dlList:
        aList = dl.xpath("dt/a")
        for a in aList:
            text = a.text
            href = a.attrib.get("href")

            sql = "insert into lb_food_class ( name , level , url ) values ( %s, %s, %s)"
            params = (text, 1, href)
            print(sql % params)
            MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodClass2():
    """
        爬取第二分类
    """
    sql = "select url, id  from lb_food_class where level = %s"
    params = (1,)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        url, parentId = row
        # print (url, parentId)
        content = getContent(url)
        dlList = content.xpath('//div[@class="main"]/div/div/dl')
        for dl in dlList:
            tag = dl.xpath("dt")[0].text
            aList = dl.xpath("dd/a")
            for a in aList:
                text = a.text
                href = a.attrib.get("href")
                sql = "insert into lb_food_class ( name , parent_id , level , url , tag) values ( %s, %s, %s, %s, %s)"
                params = (text, parentId, 2, href, tag)
                print(sql % params)
                MysqlHelper.MysqlHelper().cud(sql, params)


def getContent(url):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    return content


def loadFoodPages():
    """
       爬取页码
    """
    sql = "select url, id  from lb_food_class where level = %s and total_page = %s"
    params = (2, 0)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        url, id = row
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        request = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(request).read()

        pattern = re.compile('共\d*页')
        pages = pattern.findall(html)

        for page in pages:
            page = page.replace("共", "").replace("页", "")

            sql = "update lb_food_class set total_page =%s where id = %s"
            params = (page, id)
            print(sql % params)
            MysqlHelper.MysqlHelper().cud(sql, params)

        # 休眠1秒
        time.sleep(1)


if __name__ == "__main__":
    # 爬取第一分类
    # loadFoodClass1()

    # 爬取第二分类
    # loadFoodClass2()

    # 爬取页码
    loadFoodPages()
