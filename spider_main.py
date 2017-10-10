#coding=utf8
import time

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls=url_manager.UrlManager()
        self.downloader=html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser()
        self.outputer=html_outputer.HtmlOutputer()
    def craw(self,root_url):
        count=1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:

                new_url=self.urls.get_new_url()
                print('craw %d : %s'%(count,new_url))

                html_cont=self.downloader.download(new_url)

                new_urls,new_data=self.parser.parse(new_url,html_cont)

                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                count=count+1
                time.sleep(2)

            except:
                print('craw failed')
            # http://www.xiangrikui.com/chazhao/0_1_0_0_0_0.html?page=1

        self.outputer.outputer_html()


if __name__=="__main__":
    base_url="http://www.xyz.cn/mall/jiankangxian"
    obj_spider=SpiderMain()
    ID=1
    # 多页面爬虫
    # while ID<=8:
    #     root_url = base_url + '/p' + str(ID) + '.html'
    #     obj_spider.craw(root_url)
    #     ID = ID+1
    # 单页面爬虫测试
    root_url = base_url + '/p' + str(ID) + '.html'
    obj_spider.craw(root_url)


