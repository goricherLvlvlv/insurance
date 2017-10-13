# coding=utf8
import json
import time
from urllib.parse import urljoin
from urllib.request import urlopen

from pymongo import MongoClient
from bs4 import BeautifulSoup


def download(url):  # url下载
    if url is None:
        return None
    response = urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()


class UrlManager(object):  # url管理器类
    def __init__(self):
        self.new_urls = set()  # 未被爬取的url串
        self.old_urls = set()  # 已被爬取的url串

    def add_new_url(self, url):  # 将一条新的url加入url串里
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):  # 添加新的url串
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):  # 是否含有url
        return len(self.new_urls) != 0

    def get_new_url(self):  # 从url串中获取一条新的url
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url


class HtmlParser(object):  # 爬虫的解析器类
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')  # 配置网页解析器
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        if page_url.split('/p')[0] == 'http://www.xyz.cn/mall/jiankangxian':  # 判断是否为主页面,若是则去获取跳转页面
            # 若为保险页面则无需去获取跳转页面
            new_urls = set()
            links = soup.find_all('a', class_="hazardC_pro_toSee dev_trialSuccess")  # 获取所有"去看看"按钮的跳转页面的标签
            for link in links:
                new_url = link['href']
                new_full_url = urljoin(page_url, new_url)  # 用page_url和href来拼接保险页面的完整的url
                new_urls.add(new_full_url)
            return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {'url': page_url}
        l = page_url.split('/')

        connection = MongoClient('localhost', 27017)  # 数据库连接
        db = connection.insurance
        collection = db.XYZ

        if l[4] != "jiankangxian":  # 判断是否为保险页面,若是则获取下面的数据
            # 该区域代码还未写完 后续需要添加数据库
            title_node = soup.find('h1', class_="product-intro__title-text")
            res_data['title'] = title_node.get_text(strip=True)

<<<<<<< HEAD
            title_info = soup.find_all('div',class_="hc-form-item hc-clearFix")     # 产品特色 承保年龄...
=======
            title_info = soup.find_all('div', class_="hc-form-item hc-clearFix")  # 产品特色 承保年龄...
            # res_data['on_sale'] = title_info[0]
>>>>>>> ae67e4fdb01bf4870d586a0eaa3bace0f6f99b3f
            title_info.pop(0)
            res_data['info'] = title_info
            product_spe = ''
            for info in res_data['info']:
<<<<<<< HEAD
                product_spe+=info.get_text(strip=True)
            safeguard_content_temp = soup.find('input', id='dev_benefitesCategoryJson').get('value')      # 获取'保障内容'json数据
            insurance_notice_temp = soup.find_all('div', class_='product-detail__content hc-ckeditor')     # 获取'投保须知'
=======
                product_spe += info.get_text(strip=True)
            # json_info={'info':info_summary}
            # collection.insert({'title': res_data['title'], 'url': res_data['url'], 'product_special': product_spe})
            collection.update({'title': res_data['title']}, {
                '$set': {'title': res_data['title'], 'url': res_data['url'],
                         'product_special': product_spe}})  # 添加数据到数据库
            safeguard_content = soup.find('input', id='dev_benefitesCategoryJson').get('value')  # 获取'保障内容'json数据
            insurance_notice_temp = soup.find_all('div', class_='product-detail__content hc-ckeditor')  # 获取'投保须知'
>>>>>>> ae67e4fdb01bf4870d586a0eaa3bace0f6f99b3f
            insurance_notice_temp.pop(0)
            insurance_notice = ''
            for notice in insurance_notice_temp:
                insurance_notice += notice.get_text(strip=True)
<<<<<<< HEAD
            json_datas=json.loads(safeguard_content_temp)
            safeguard_content=[]

            for json_data in json_datas:
                for a_data in json_data['protectPropDTOs']:
                    print(a_data['optionDTOs'])
                    safeguard_content+=[{'name':a_data['name'],'explanation':a_data['explanation']}]
            #collection.insert({'title': res_data['title'], 'url': res_data['url'], 'product_special': product_spe})
            collection.update({'title': res_data['title']}, {'$set': {'title': res_data['title'], 'url': res_data['url'],'product_special': product_spe}})        # 添加数据到数据库
            collection.update({'title':res_data['title']},{'$set':{'safeguard_content': safeguard_content,'insurance':insurance_notice}})      # 将'保障内容'与'投保须知'加如数据库
                                                                                                            # '保障内容'中含有大量无用数据,且保障内容的json格式 在数据库中没有良好的体现
            #collection.remove()  # 删除数据库

=======
            # print(safeguard_content)
            collection.update({'title': res_data['title']}, {'$set': {'safeguard_content': safeguard_content}})
            collection.update({'title': res_data['title']},
                              {'$set': {'insurance': insurance_notice}})  # 将'保障内容'与'投保须知'加如数据库
            # '保障内容'中含有大量无用数据,且保障内容的json格式 在数据库中没有良好的体现
            # collection.remove()  # 删除数据库
>>>>>>> ae67e4fdb01bf4870d586a0eaa3bace0f6f99b3f
        return res_data


class SpiderMain(object):  # 爬虫类
    def __init__(self):
        self.parser = HtmlParser()
        self.urls = UrlManager()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)  # 将根url添加到url串里
        while self.urls.has_new_url():
            try:
<<<<<<< HEAD
                new_url=self.urls.get_new_url()     # url串里弹出url
                print('craw %d : %s'%(count,new_url))       # 输出对应的保险序号以及网址
                html_cont=download(new_url)     # 下载网页内容
                new_urls,new_data=self.parser.parse(new_url,html_cont)      # 把content传入parser中爬取各保险的网址
                                                                            # 或者爬取保险页面的内容 分别赋值给new_urls和new_data
                self.urls.add_new_urls(new_urls)        # 若成功爬取new_urls,将获取的url串加入url管理器的url串中
                count=count+1       # 计数器加1
                time.sleep(1.5)       # 当前网页不能接受过于频繁的访问,延迟+1s 0--0
=======
                new_url = self.urls.get_new_url()  # url串里弹出url
                print('craw %d : %s' % (count, new_url))  # 输出对应的保险序号以及网址
                html_cont = download(new_url)  # 下载网页内容
                new_urls, new_data = self.parser.parse(new_url, html_cont)  # 把content传入parser中爬取各保险的网址
                # 或者爬取保险页面的内容 分别赋值给new_urls和new_data
                self.urls.add_new_urls(new_urls)  # 若成功爬取new_urls,将获取的url串加入url管理器的url串中
                count = count + 1  # 计数器加1
                time.sleep(1)  # 当前网页不能接受过于频繁的访问,延迟+1s 0--0
>>>>>>> ae67e4fdb01bf4870d586a0eaa3bace0f6f99b3f

            except:
                print('craw failed')


if __name__ == "__main__":
    base_url = "http://www.xyz.cn/mall/jiankangxian"
    obj_spider = SpiderMain()
    ID = 1
    # 单页面爬虫测试
    # root_url = base_url + '/p' + str(ID) + '.html'
    # obj_spider.craw(root_url)
    # 多页面爬虫
    while ID <= 8:
        root_url = base_url + '/p' + str(ID) + '.html'
        obj_spider.craw(root_url)
        ID = ID + 1
