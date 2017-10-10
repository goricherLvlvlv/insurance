
from urllib.request import urlopen

import demjson as demjson
from bs4 import BeautifulSoup

html=urlopen('http://www.xyz.cn/mall/detail-jiuwjpogpp.html')
html_content=html.read().decode('gbk')
bs=BeautifulSoup(html_content,"html.parser")
table_summary=bs.find(attrs={'id':'dev_benefitesCategoryJson'})['value']
# trs=table_summary.find_all('tr')
# for sibling in table_summary[0].tr.next_siblings:
#     print(sibling)
# for table in table_summary:
#     trs=table.find_all()
#     for td in trs:
#         print(td)

# print(table_summary)

text = demjson.decode(table_summary)
print(text)
