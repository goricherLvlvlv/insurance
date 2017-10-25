# coding=utf8
import json
import time
from queue import Queue
from urllib.parse import urljoin
from urllib.request import urlopen
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
"""
base_url用于访问主页面
root_url用于拼接出对应的保险页面
URL_QUEUE是存储url的队列
"""
base_url = "https://baoxian.taobao.com/nv/itemList.html?page=1&insType=health"
root_url = "https://baoxian.taobao.com"
URL_QUEUE = Queue()
"""
对队列里每一个url使用craw_main()方法获得数据
"""
def craw():
    while not URL_QUEUE.empty():
        url = URL_QUEUE.get()
        craw_main(url)
        URL_QUEUE.task_done()

"""
通过API获取json数据
再把json数据转为字典类型,再加入数据库(未完成)
"""
def craw_main(url):
    url_json = "https://baoxian.taobao.com/json/item/insuredProject.do"
    querystring = {"item_id": url.split('=')[1]}
    response = requests.request("GET", url_json, params=querystring)
    json_dics = json.loads(response.text)
    print(json_dics)
if __name__ == "__main__":
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text,'lxml')
    """
    获得所有a标签,然后遍历a标签得到href的值
    page表示保险的页面 输出保险页面,得知保险在某个保险页面
    将首页的URL加入队列中,然后运行craw()方法获取数据
    while循环重复前面的操作,把剩下的页面做如上处理
    """
    all_a = soup.find_all(class_ ="il-price-buy")
    all_href = list()
    for one_a in all_a:
        all_href.append(one_a['href'])
    page = 1;
    print("page %d" % (page))
    for one_href in all_href:
        URL_QUEUE.put(root_url+one_href)
    craw()
    while(1):
        try:url = soup.find('a', class_="next ")['href']
        except:
            page = page + 1
            print("page %d" % (page))
            print("该页面没有保险")
            break
        response = requests.get(root_url + url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_a = soup.find_all(class_="il-price-buy")
        all_href = list()
        for one_a in all_a:
            all_href.append(one_a['href'])
        for one_href in all_href:
            URL_QUEUE.put(root_url + one_href)
        page = page + 1
        print("page %d" % (page))
        craw()