import re
from urllib.parse import urljoin

import time
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')

        new_urls = self._get_new_urls(page_url,soup)

        new_data = self._get_new_data(page_url,soup)

        return new_urls,new_data

    #<a href="/mall/detail-jiuwjpogpp.html" feeitems="" price="100.00|100.00" title="" target="_blank" class="hazardC_pro_toSee dev_trialSuccess">
    #     去看看
    # </a>
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # links = soup.find_all('a',href=re.compile(r"/mall/detail"))

        links = soup.find_all('a',class_="hazardC_pro_toSee dev_trialSuccess")

        for link in links:

            new_url = link['href']
            new_full_url = urljoin(page_url,new_url)
            new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url']=page_url
        l = page_url.split('/')

        if l[4]!="jiankangxian":

            title_node = soup.find('h1',class_="product-intro__title-text")
            res_data['title'] = title_node.get_text()
            title_info = soup.find_all('div',class_="hc-form-item hc-clearFix")
            res_data['on_sale'] = title_info[0]
            title_info.pop(0)
            #title_info.pop(-1)
            res_data['info'] = title_info
            #<table width="100%" cellpadding="0" cellspacing="0">
            summary = soup.find_all('table', width="100%", cellpadding="0", cellspacing="0")
            # summary_tb=summary[0]
            # summary_tds=summary_tb.find_all('tr')
            res_data['summary'] = summary
            for sibling in soup.find("table").tr.next_siblings:
                print(sibling)

            # summary_node = soup.select_one('.contentBox-item')
            # res_data['summary'] = summary_node


        return res_data