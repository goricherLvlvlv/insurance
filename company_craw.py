# -*- coding: utf-8 -*-
from queue import Queue
from urllib.request import urlopen

import time
from bs4 import BeautifulSoup
import requests
URL_QUEUE = Queue()
ROOT_URL = 'http://www.xyz.cn'


# 获取url列表并放入队列
def url_craw():
    # 首页url地址
    first_page_url = "/mall/jiankangxian/"

    response = requests.get(ROOT_URL + first_page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    # pager为网页分页信息的div，从这里找到所有的a标签
    all_a = soup.find('div', class_="pager").find_all('a')
    #print(all_a)
    all_href=list()
    for one_a in all_a:
        all_href.append(one_a.get('href'))
    all_href=list(set(all_href))
    all_href.sort()
    #print(all_href)
    """
    输出示例:
        /mall/jiankangxian/p2.html <------注意默认不包含第一页，处理时先将第一页入队列
        /mall/jiankangxian/p3.html
        /mall/jiankangxian/p4.html
        /mall/jiankangxian/p5.html
        /mall/jiankangxian/p6.html
        /mall/jiankangxian/p7.html
        /mall/jiankangxian/p8.html
        /mall/jiankangxian/p2.html <------注意这个url是下一页所在的a标签链接。遍历时请切片处理
    """
    # 处理之前先将首页入队列
    URL_QUEUE.put(ROOT_URL + first_page_url)
    # 因为pager中包含了下一页的url，因此这个循环得先将all_a切片，即只将前n - 1个url放入队列
    for one_href in all_href:
        URL_QUEUE.put(ROOT_URL + one_href)

# 工作线程，主要是读队列中url并调用company_craw方法爬虫获取产品url和对应的公司name
def get_company_craw(d_url_company):
    while not URL_QUEUE.empty():
        url = URL_QUEUE.get()
        company_craw(url,d_url_company)
        URL_QUEUE.task_done()


# 获取保险公司名和对应url的爬虫
def company_craw(url,d_url_company):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # 找到所有的li标签，每个li标签里存了各个保险产品的信息，包括了保险产品所在的保险公司名和对应的详情页url
    all_ul = soup.find_all('ul', class_='hazardC_pro_con_list')
    for one_ul in all_ul:
        all_li=one_ul.find_all('li',class_='hazardC_pro_con_item')
    # 这里需要遍历每一个li，即遍历每个产品的信息，取出其中的公司名和url信息。这样做保证了公司名和url一一对应
    #print(all_li)
    for one_li in all_li:
        company_name = one_li.find_all('span', class_='hazardC_pro_con_company')[0].a.get_text(strip=True)
        product_url = one_li.find_all('a', class_='f16 dev_trialSuccess')[0]['href']
        #print(company_name, product_url)
        d_url_company[ROOT_URL + product_url] = company_name;
    time.sleep(2)

def company_main():
    url_craw()
    d_url_company = dict()
    get_company_craw(d_url_company)
    #print(d_url_company)
    return d_url_company


