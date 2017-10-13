import requests
from bs4 import BeautifulSoup

try:
    header={'user-agent':'Mozilla/5.0'}
    base_url='http://www.xyz.cn/mall/jiankangxian/'
    ID = 1
    while ID <= 8:
        root_url = base_url + '/p' + str(ID) + '.html'
        t1=requests.get(root_url,headers=header,timeout=300)
        soup=BeautifulSoup(t1.text,"html.parser")
        i=0
        count = 0
        new_companys=[]
        name=[]
        b=soup.find('div',id='dev_prodList')
        all_c=b.find_all('span',class_='hazardC_pro_con_company')
        d_all=b.find_all('a',class_='f16 dev_trialSuccess')
        for d in d_all:
            name.append(d.text.strip())

        for c in all_c:
            new_companys.append(c.text.strip())
            count = count +1
            print(count, name[i],'  ',new_companys[i])
            i=i+1
        ID = ID+1
except:
    print("网络出现错误或连接超时！")
    c=input()