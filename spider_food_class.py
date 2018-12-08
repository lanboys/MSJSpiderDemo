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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/54.0.2840.99 Safari/537.36"
}


def getContent(url):
    request = urllib2.Request(url, headers=headers)
    return etree.HTML(urllib2.urlopen(request).read())


def loadFoodClass1():
    """
        爬取第一分类
    """
    url = "https://www.meishij.net/jiankang/"
    dlList = getContent(url).xpath('//div[@class="nav"]/ul/li[2]/div/div/div/dl')

    for dl in dlList:
        aList = dl.xpath("dt/a")
        for a in aList:
            text = a.text
            class_url = a.attrib.get("href")

            sql = "insert into lb_food_class ( name , level , class_url ) values ( %s, %s, %s)"
            params = (text, 1, class_url)
            print(sql % params)
            MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodClass2():
    """
        爬取第二分类
    """
    sql = "select class_url, id  from lb_food_class where level = %s"
    params = (1,)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        class_url, parentId = row
        # print (url, parentId)
        dlList = getContent(class_url).xpath('//div[@class="main"]/div/div/dl')
        for dl in dlList:
            tag = dl.xpath("dt/text()")[0]
            aList = dl.xpath("dd/a")
            for a in aList:
                text = a.text
                class_url = a.attrib.get("href")
                sql = "insert into lb_food_class ( name , parent_id , level , class_url , tag)" \
                      " values ( %s, %s, %s, %s, %s)"
                params = (text, parentId, 2, class_url, tag)
                print(sql % params)
                MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodPages():
    """
       爬取页码
    """
    sql = "select class_url, id  from lb_food_class where level = %s and total_page = %s"
    params = (2, 0)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        class_url, id = row
        request = urllib2.Request(class_url, headers=headers)
        html = urllib2.urlopen(request).read()

        page = re.compile(r'共(\d*)页').match(html).group(1)

        sql = "update lb_food_class set total_page =%s where id = %s"
        params = (page, id)
        print(sql % params)
        MysqlHelper.MysqlHelper().cud(sql, params)

        # 休眠1秒
        time.sleep(1)


def loadFoodList():
    sql = "select id, parent_id, class_url, total_page, current_page  from lb_food_class where level = %s " \
          "and total_page > current_page and parent_id not in (6, 7)"
    loadFoodListComm(sql, 1)


def loadFoodMaterialList():
    sql = "select id, parent_id, class_url, total_page, current_page  from lb_food_class where level = %s " \
          "and total_page > current_page and parent_id in (7, 7)"
    loadFoodListComm(sql, 2)


def loadFoodListComm(sql, type):
    params = (2,)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        id, parent_id, url, total_page, current_page = row

        # total_page = total_page - 30
        # if total_page < current_page:
        #     total_page = current_page + 5

        for page in range(current_page + 1, total_page + 1):
            page_ = "?&page="
            if "?" in url:
                page_ = "&page="
            # 爬取每页数据
            if type == 1:
                loadFoodListPage(url + page_ + str(page), id, parent_id)
            else:
                loadFoodMaterialListPage(url + page_ + str(page), id, parent_id)
            # 更新页码
            updateCurrentPage(id, page)
            # 休眠1秒
            time.sleep(1)


def updateCurrentPage(id, currentPage):
    sql = "update lb_food_class set current_page =%s where id = %s"
    params = (currentPage, id)
    print(sql % params)
    MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodListPage(url, class1_id, class2_id):
    print (url)
    divList = getContent(url).xpath('//div[@class="listtyle1"]/a')
    for div in divList:
        html_url = div.xpath("./@href")[0]
        title = div.xpath("./@title")[0]
        thumbnail_url = div.xpath("img/@src")[0]

        comment_num = 0
        popularity_num = 0
        spanTextList = div.xpath("div//span/text()")
        for spanText in spanTextList:
            span = spanText.replace(" ", "").encode("utf-8")
            m = re.compile(r'(\d*)评论(\d*)人气').match(span)
            if m is not None:
                comment_num = m.group(1)
                popularity_num = m.group(2)

        step_num = 0
        liTextList = div.xpath("div//li[@class='li1']/text()")
        for liText in liTextList:
            step = liText.replace(" ", "").encode("utf-8")
            m = re.compile(r'(\d*)步').match(step)
            if m is not None:
                step_num = m.group(1)

        sql = "insert into lb_food ( name , class1_id , class2_id , comment_num , popularity_num ," \
              " step_num , html_url , thumbnail_url) values ( %s, %s, %s, %s, %s, %s, %s, %s )"
        params = (
            title, class1_id, class2_id, comment_num, popularity_num, step_num, html_url,
            thumbnail_url)
        # print(sql % params)
        MysqlHelper.MysqlHelper().cud(sql, params)


def loadFoodMaterialListPage(url, class1_id, class2_id):
    print (url)
    divList = getContent(url).xpath('//div[@class="listtyle1"]')
    for div in divList:
        html_url = div.xpath('div[@class="img"]/a/@href')[0]
        logo_url = div.xpath("div/a/img/@src")[0]
        title = div.xpath('div[@class="info1"]/h3/a/text()')[0]
        description = ""
        descriptionList = div.xpath('div[@class="info1"]/div/span/text()')
        for d in descriptionList:
            description = d

        sql = "insert into lb_food_material ( name , class1_id , class2_id ,description, html_url," \
              " logo_url) values ( %s, %s, %s, %s, %s, %s)"
        params = (title, class1_id, class2_id, description, html_url, logo_url)
        # print(sql % params)
        MysqlHelper.MysqlHelper().cud(sql, params)


if __name__ == "__main__":
    # 爬取第一分类
    # loadFoodClass1()

    # 爬取第二分类
    # loadFoodClass2()

    # 爬取页码
    # loadFoodPages()

    # 爬取第二分类下菜品列表信息
    # loadFoodList()

    # 爬取第二分类下菜品材料列表信息
    loadFoodMaterialList()
