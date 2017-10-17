import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

try:
    header = {'user-agent': 'Mozilla/5.0'}
    base_url = 'http://www.xyz.cn/mall/jiankangxian/'
    ID = 1
    while ID <= 8:
        root_url = base_url + '/p' + str(ID) + '.html'
        t1 = requests.get(root_url, headers=header, timeout=300)
        soup = BeautifulSoup(t1.text, "html.parser")
        i = 0
        count = 0
        names = []
        new_companys = []
        new_urls = []
        b = soup.find('div', id='dev_prodList')
        all_companys = b.find_all('span', class_='hazardC_pro_con_company')
        all_names = b.find_all('a', class_='f16 dev_trialSuccess')

        links = soup.find_all('a', class_="hazardC_pro_toSee dev_trialSuccess")  # 获取所有"去看看"按钮的跳转页面的标签
        for link in links:
            new_url = link['href']
            new_urls = urljoin(root_url, new_url)  # 用page_url和href来拼接保险页面的完整的url

        for d in all_names:  # 获取产品名称
            names.append(d.text.strip())

        for c in all_companys:  # 获取产品对应的公司
            new_companys.append(c.text.strip())
            count = count + 1
            print(count, names[i], '  ', new_companys[i], '  ', new_urls)  # 输出产品名，公司，及url
            i = i + 1
        ID = ID + 1
except:
    print("网络出现错误或连接超时！")
    c = input()
