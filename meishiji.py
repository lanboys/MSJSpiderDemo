# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2

from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')


def loadPage(url):
    """
        作用：根据url发送请求，获取服务器响应文件
        url: 需要爬取的url地址
    """
    # print url
    # headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}

    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    # 解析HTML文档为HTML DOM模型
    content = etree.HTML(html)
    # print content
    # 返回所有匹配成功的列表集合
    link_list = content.xpath('//div[@class="listtyle1"]')

    for item in link_list:
        # test = item.xpath("/a/@target")
        # print(type(test))
        # test = test[0]
        # print(type(test))

        title = item.xpath("a/@title")[0]
        goods_url = item.xpath("a/@href")[0]
        img_url = item.xpath("a/img/@src")[0]

        goods = Goods(title, goods_url, img_url)
        print(goods)
        print("-----------------")

    # link_list = content.xpath('//a[@class="j_th_tit"]/@href')
    # for link in link_list:
    #     fulllink = "http://tieba.baidu.com" + link
    #     # 组合为每个帖子的链接
    #     # print link
    #     loadImage(fulllink)


# 取出每个帖子里的每个图片连接
def loadImage(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    request = urllib2.Request(link, headers=headers)
    html = urllib2.urlopen(request).read()
    # 解析
    content = etree.HTML(html)
    # 取出帖子里每层层主发送的图片连接集合
    # link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    # link_list = content.xpath('//div[@class="post_bubble_middle"]')
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    # 取出每个图片的连接
    for link in link_list:
        # print link
        writeImage(link)


def writeImage(link):
    """
        作用：将html内容写入到本地
        link：图片连接
    """
    # print "正在保存 " + filename
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # 文件写入
    request = urllib2.Request(link, headers=headers)
    # 图片原始数据
    image = urllib2.urlopen(request).read()
    # 取出连接后10位做为文件名
    filename = link[-10:]
    # 写入到本地磁盘文件内
    with open("files/" + filename, "wb") as f:
        f.write(image)
    print "已经成功下载 " + filename


def tiebaSpider(url, beginPage, endPage):
    """
        作用：贴吧爬虫调度器，负责组合处理每个页面的url
        url : 贴吧url的前部分
        beginPage : 起始页
        endPage : 结束页
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        # filename = "第" + str(page) + "页.html"
        fullurl = url + "&page=" + str(pn)
        # print fullurl
        loadPage(fullurl)
        # print html

        print "谢谢使用"


class Goods:

    def __init__(self, title, url, imgUrl):
        self.__title = title
        self.__url = url
        self.__imgUrl = imgUrl

    def __str__(self):
        return "标题：" + self.__title + " 链接: " + self.__url + " logo : " + self.__imgUrl


if __name__ == "__main__":
    # beginPage = int(raw_input("请输入起始页："))
    # endPage = int(raw_input("请输入结束页："))

    beginPage = 1
    endPage = 1

    url = "https://www.meishij.net/chufang/diy/jiangchangcaipu/?"
    tiebaSpider(url, beginPage, endPage)
