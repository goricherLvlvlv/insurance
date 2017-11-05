# coding=utf8
import json
import re
import types
from queue import Queue
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
connection = MongoClient('localhost', 27017)  # 数据库连接
db = connection.insurance
collection = db.Taobao
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
下载各类pdf,doc,xlsx文件和图片
防止未来网站改变地址而导致无法浏览
fileurl是文件的下载地址
title为文件命名
document决定了文件储存的文件夹是哪个
"""
def download(fileurl,title,document):
    r = requests.get(fileurl, stream=True)
    """
    filename0是去除'/'的filename
    """
    filename0 = str()
    title = title.split('/')
    for one in title:
        filename0 = filename0 + one
    """
    filename1是去除'|'的filename
    """
    filename1 = str()
    filename0 = filename0.split('|')
    for one in filename0:
        filename1 = filename1 + one

    with open("D:\python project\insurance\download\\"+document+"\\"+filename1+'.'+fileurl.split('.')[-1], "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print("%s downloaded!\n" % filename1)
def down_html(url):
    down_html()
"""
使用了以下两种匹配符:
    .国华的正则匹配符
    如"2016.4.1启用"以及"2016.4.1号启用"字符串的正则匹配符
将字典转化为字符串
使用re.sub()把key值中可能的点号去除或者改为下划线
防止无法加入mongodb
"""
def delete_dot(json_dics):
    json_str = str(json_dics)
    s1 = r"\.\u56fd\u534e"
    s2 = r"\d\.\d\.\d\u542f\u7528"
    s3 = r"\d\.\d\.\d\u53f7\u542f\u7528"
    json_str = re.sub(s1, '_国华', json_str)
    json_str = re.sub(s2, '',json_str)
    json_str = re.sub(s3, '',json_str)
    return json_str
"""
通过API获取json数据
再把json数据转为字典类型,再加入数据库(未完成)
"""
def craw_main(url):
    url_json = "https://baoxian.taobao.com/json/item/insuredProject.do"
    querystring = {"item_id": url.split('=')[1]}
    response = requests.request("GET", url_json, params=querystring)
    json_dics = json.loads(response.text)
    """
    调用delete_dot方法,去除点号
    返回一个string的数据,再用eval方法转为字典
    """
    json_str = delete_dot(json_dics)
    json_dics = eval(json_str)
    """
    获取title
    再通过title获取公司名字
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    title = soup.find('title').get_text(strip=True)
    company = title.split('】')[0][1:]
    """
    将数据添加到数据库
    """
    collection.insert({'title':title,'url':url,'company':company,'information':json_dics})
    #collection.update({'url': url}, {'$set':{'title':title,'url':url,'company':company,'information':json_dics}})
    """
    正则表达式r"(http.+?)([.]doc|[.]pdf)" 匹配http(s)://...pdf||doc(x)||xls(x)的url
    把url递给储存给file_urls(tuple类型)
    遍历file_urls,调用download方法,文件名为保险标题+ID的格式
    """
    ID = 0
    for i in json_dics['data']:
        i_str = str(i['data'])
        file_urls = re.findall(r"(http.+?)([.]docx?|[.]pdf|[.]xlsx?)",i_str)
        for i in file_urls:
            file_url = ''.join(i)
            download(file_url,title + str(ID),"text")
            ID = ID + 1


    """
    图片爬取
    当一个保险里有多个html?文件时,ID0会自增,命名为page+ID0的格式
    ID1是表示该种保险的图片个数 格式为NO.+ID1
    """
    ID0 = 0
    ID1 = 0
    for i in json_dics['data']:
        i_str = str(i['data'])
        file_urls = re.findall(r"(http.+?)([.]html?)", i_str)
        for j in file_urls:
            file_url = ''.join(j)
            try:
                response = requests.get(file_url)
                soup_img = BeautifulSoup(response.text, 'lxml')
                url_img = soup_img.find('div', class_='skin-box-bd clear-fix')
                if (url_img):
                    url_img = url_img.find_all('img')
                    for k in url_img:
                        download('https:' + k.get('data-ks-lazyload'), title + 'page' + str(ID0) + '_NO.' + str(ID1),"img")
                        ID1 = ID1 + 1
                ID0 = ID0 + 1
            except:
                print("-------------------------------------------------\n该页面无法打开\n-------------------------------------------------")

if __name__ == "__main__":
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text,'lxml')
    collection.remove()
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