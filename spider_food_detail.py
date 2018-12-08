# !/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import re
import sys
import time
import urllib2

from lxml import etree

import MysqlHelper

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}


def getContent(url):
    request = urllib2.Request(url, headers=headers)
    return etree.HTML(urllib2.urlopen(request).read())


def loadFoodDetail():
    sql = "select id, html_url from lb_food where is_spider_detail = %s limit %s, %s "
    params = (0, 0, 10)
    print(sql % params)
    rows = MysqlHelper.MysqlHelper().fetchall(sql, params)

    for row in rows:
        id, html_url = row
        print(html_url)
        content = getContent(html_url)
        # 爬取基本信息
        spiderBaseInfo(id, content)
        # 爬取评论数据
        spiderComment(id, content)
        # 爬取做法
        spiderProcess(id, content)
        # 爬取用料
        spiderMaterial(id, content)

        # 更新状态
        updateSpiderDetail(id)
        # 休眠1秒
        time.sleep(1)


def updateSpiderDetail(id):
    sql = "update lb_food set is_spider_detail = 1 where id = %s "
    params = (id,)
    print(sql % params)
    MysqlHelper.MysqlHelper().cud(sql, params)


def spiderProcess(food_id, content):
    divStepList = content.xpath("//div[@class='editnew edit']/div[@class='content clearfix']")
    for div in divStepList:
        step = ""
        content = ""
        img_url = ""

        stepList = div.xpath("em/text()")
        if len(stepList) > 0:
            step = stepList[0]

        stepList = div.xpath("div/p/text()")
        if len(stepList) > 0:
            content = stepList[0]

        stepList = div.xpath("div/p/img/@src")
        if len(stepList) > 0:
            img_url = stepList[0]

        sql = "insert into lb_cook_process (food_id, step, content, img_url)" \
              " values ( %s, %s, %s, %s )"
        params = (food_id, step, content, img_url)
        # print(sql % params)
        MysqlHelper.MysqlHelper().cud(sql, params)


def spiderMaterial(food_id, content):
    divList = content.xpath("//div[@class='materials_box']/div")

    for div in divList:
        tag = div.xpath("h3/a/text()")[0]
        liList = div.xpath("ul/li")
        for li in liList:
            thumbnail_url = ""
            name = ""
            dosage = ""

            thumbnail_url_list = li.xpath("a/img/@src")
            if len(thumbnail_url_list) > 0:
                thumbnail_url = thumbnail_url_list[0]

            name_list = li.xpath("div/h4/a/text()")
            if len(name_list) > 0:
                name = name_list[0]

            if name == "":
                name_list = li.xpath("h4/a/text()")
                if len(name_list) > 0:
                    name = name_list[0]

            dosage_list = li.xpath("div/h4/span/text()")
            if len(dosage_list) > 0:
                dosage = dosage_list[0]

            if dosage == "":
                dosage_list = li.xpath("span/text()")
                if len(dosage_list) > 0:
                    dosage = dosage_list[0]

            sql = "insert into lb_food_material_assoc ( food_id , tag, name, thumbnail_url, dosage)" \
                  " values ( %s, %s, %s, %s, %s )"
            params = (food_id, tag, name, thumbnail_url, dosage)
            # print(sql % params)
            MysqlHelper.MysqlHelper().cud(sql, params)


def spiderBaseInfo(food_id, content):
    # 爬取基本信息
    logo_url = ""
    logo_url_list = content.xpath("//div/div[@class='cp_headerimg_w']/img/@src")
    if len(logo_url_list) > 0:
        logo_url = logo_url_list[0]

    # favorite_num = "未知"
    suitable_label = "未知"
    cooking_method = "未知"
    cooking_difficulty = "未知"
    people_num = "未知"
    cooking_taste = "未知"
    ready_time = "未知"
    cooking_time = "未知"
    user_avatar_url = "未知"
    user_id = "未知"
    user_url = "未知"
    user_grade = "未知"
    final_img_url = "未知"
    infoDivList = content.xpath("//div/div[@class='cp_main_info_w']")
    for div in infoDivList:
        # xpath = div.xpath("div/span[@class='favbtns']/a/span")[0]
        # favorite_num = xpath.text
        tongjiList = div.xpath("div[@class='info1']//dt/a/text()")
        for index in range(len(tongjiList)):
            suitable_label += tongjiList[index] + ","
        suitable_label = suitable_label[0:-1]

        cooking_method_list = div.xpath("div[@class='info2']/ul/li[1]//a/text()")
        if len(cooking_method_list) > 0:
            cooking_method = cooking_method_list[0]

        cooking_difficulty_list = div.xpath("div[@class='info2']/ul/li[2]//a/text()")
        if len(cooking_difficulty_list) > 0:
            cooking_difficulty = cooking_difficulty_list[0]

        people_num_list = div.xpath("div[@class='info2']/ul/li[3]//a/text()")
        if len(people_num_list) > 0:
            people_num = people_num_list[0]

        cooking_taste_list = div.xpath("div[@class='info2']/ul/li[4]//a/text()")
        if len(cooking_taste_list) > 0:
            cooking_taste = cooking_taste_list[0]

        ready_time_list = div.xpath("div[@class='info2']/ul/li[5]//a/text()")
        if len(ready_time_list) > 0:
            ready_time = ready_time_list[0]

        cooking_time_list = div.xpath("div[@class='info2']/ul/li[6]//a/text()")
        if len(cooking_time_list) > 0:
            cooking_time = cooking_time_list[0]

        user_avatar_url = div.xpath("div[@class='info3']/div[@class='user']/a/img/@src")[0]
        user_url = div.xpath("div[@class='info3']/div[@class='user']/a/@href")[0]
        if user_url is not None:
            m = re.compile(r'.*id=(\d*)').match(user_url)
            if m is not None:
                user_id = m.group(1)

        ug = div.xpath("div[@class='info3']//div[@class='info']/h4/a/@title")
        if len(ug) > 0:
            user_grade = ug[0]
    materials_desc = content.xpath("string(//div/div/div[@class='materials']/p)")
    # 爬取成品图
    final_img_url_list = list(
        set(content.xpath("//div[@class='swiper-wrapper swiper-wrapper1']/div/img/@src")))
    for fiu in final_img_url_list:
        final_img_url += fiu + ","
    final_img_url = final_img_url[0:-1]
    cooking_skill = content.xpath("string(//div[@class='editnew edit']/p)")
    # print (logo_url)
    # print (favorite_num)
    # print (suitable_label)
    # print (cooking_method)
    # print (cooking_difficulty)
    # print (people_num)
    # print (cooking_taste)
    # print (ready_time)
    # print (cooking_time)
    # print (user_url)
    # print (user_avatar_url)
    # print (user_id)
    # print (user_grade)
    # print (materials_desc)
    # print (final_img_url)
    # print (cooking_skill)
    sql = "update lb_food set logo_url = %s, suitable_label = %s, cooking_method = %s, cooking_difficulty = %s," \
          " people_num = %s, cooking_taste = %s, ready_time = %s, cooking_time = %s, user_url = %s, " \
          "user_avatar_url = %s, user_id = %s, user_grade = %s, materials_desc = %s, final_img_url = %s," \
          " cooking_skill = %s where id = %s"
    params = (
        logo_url, suitable_label, cooking_method, cooking_difficulty, people_num, cooking_taste,
        ready_time, cooking_time, user_url, user_avatar_url, user_id, user_grade, materials_desc,
        final_img_url, cooking_skill, food_id)
    # print(sql % params)
    MysqlHelper.MysqlHelper().cud(sql, params)


def spiderComment(food_id, content):
    # 爬取评论数据
    comlist = content.xpath("//div[@class='cp_comlist_w']/ul/li")
    for c in comlist:
        content = c.xpath(".//p/strong")[0].tail.encode("utf-8").strip()

        commentTime = ""
        time = c.xpath(".//div/span/text()")[0].encode("utf-8")
        m = re.compile(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})来自').findall(time)
        if len(m) > 0:
            commentTime = m[0]
        comment_time = datetime.datetime.strptime(commentTime, '%Y-%m-%d %H:%M:%S')

        user_name = c.xpath("a/h5/text()")[0]
        user_avatar_url = c.xpath("a/img/@src")[0]

        comHref = c.xpath("a/@href")

        user_id = ""
        user_url = ""

        if len(comHref) > 0:
            com_user_url = comHref[0]
            m = re.compile(r'.*id=(\d*)').match(com_user_url)
            if m is not None:
                user_id = m.group(1)
                user_url = com_user_url

        # print(comment)
        # print(comment_time)
        # print(user_name)
        # print(user_avatar_url)
        # print(user_id)
        # print(user_url)

        sql = "insert into lb_food_comment ( food_id , user_name , user_id , user_avatar_url ," \
              " user_url, content, comment_time) values ( %s, %s, %s, %s, %s, %s, %s)"
        params = (food_id, user_name, user_id, user_avatar_url, user_url, content, comment_time)
        # print(sql % params)
        MysqlHelper.MysqlHelper().cud(sql, params)


if __name__ == "__main__":
    # 爬取菜品详情
    loadFoodDetail()
