#coding=utf8
import time
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup

def download(url):        # url下载
    if url is None:
        return None
    response = urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()

class UrlManager(object):       # url管理器类
    def __init__(self):
        self.new_urls=set()     # 未被爬取的url串
        self.old_urls=set()     # 已被爬取的url串
    def add_new_url(self, url):     # 将一条新的url加入url串里
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    def add_new_urls(self, urls):       # 添加新的url串
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    def has_new_url(self):      # 是否含有url
        return len(self.new_urls) != 0
    def get_new_url(self):      # 从url串中获取一条新的url
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

class HtmlParser(object):       # 爬虫的解析器类
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')     # 配置网页解析器
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data
    def _get_new_urls(self, page_url, soup):
        if(page_url.split('/p')[0]=='http://www.xyz.cn/mall/jiankangxian'):     # 判断是否为主页面,若是则去获取跳转页面
                                                                                      # 若为保险页面则无需去获取跳转页面
            new_urls = set()
            links = soup.find_all('a',class_="hazardC_pro_toSee dev_trialSuccess")      # 获取所有"去看看"按钮的跳转页面的标签
            for link in links:
                new_url = link['href']
                new_full_url = urljoin(page_url,new_url)        # 用page_url和href来拼接保险页面的完整的url
                new_urls.add(new_full_url)
            return new_urls
    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url']=page_url
        l = page_url.split('/')
        if l[4]!="jiankangxian":        # 判断是否为保险页面,若是则获取下面的数据
                                          # 该区域代码还未写完 后续需要添加数据库
            title_node = soup.find('h1',class_="product-intro__title-text")
            res_data['title'] = title_node.get_text()
            title_info = soup.find_all('div',class_="hc-form-item hc-clearFix")
            res_data['on_sale'] = title_info[0]
            title_info.pop(0)
            res_data['info'] = title_info
        return res_data

class SpiderMain(object):       # 爬虫类
    def __init__(self):
        self.parser = HtmlParser()
        self.urls=UrlManager()
    def craw(self,root_url):
        count=1
        self.urls.add_new_url(root_url)     # 将根url添加到url串里
        while self.urls.has_new_url():
            try:
                new_url=self.urls.get_new_url()     # url串里弹出url
                print('craw %d : %s'%(count,new_url))       # 输出对应的保险序号以及网址

                html_cont=download(new_url)     # 下载网页内容

                new_urls,new_data=self.parser.parse(new_url,html_cont)      # 把content传入parser中爬取各保险的网址
                                                                            # 或者爬取保险页面的内容 分别赋值给new_urls和new_data

                self.urls.add_new_urls(new_urls)        # 若成功爬取new_urls,将获取的url串加入url管理器的url串中

                count=count+1       # 计数器加1
                time.sleep(1)       # 当前网页不能接受过于频繁的访问,延迟+1s 0--0

            except:
                print('craw failed')


if __name__=="__main__":
    base_url="http://www.xyz.cn/mall/jiankangxian"
    obj_spider = SpiderMain()
    ID=1
    # 单页面爬虫测试
    root_url = base_url + '/p' + str(ID) + '.html'
    obj_spider.craw(root_url)
    # 多页面爬虫
    # while ID<=8:
    #     root_url = base_url + '/p' + str(ID) + '.html'
    #     obj_spider.craw(root_url)
    #     ID = ID+1
