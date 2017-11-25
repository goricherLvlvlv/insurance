import xlwt
from pymongo import MongoClient
if __name__=='__main__':
    conn = MongoClient('localhost', 27017)
    db = conn.insurance#数据库，没有则自动创建
    my_set = db.Taobao #使用test_set集合，没有则自动创
    for i_set in my_set.find():
        print(i_set['title'],i_set['information']['data'][0]['data']['desc'],i_set['information']['data'][0]['data']['plan'],i_set['years'])
    workbook = xlwt.Workbook(encoding='ascii')
    sheet = workbook.add_sheet('sheet1')
    row = 0
    for i_set in my_set.find():
        sheet.write(row, 0, str(i_set['title']))
        sheet.write(row, 1, str(i_set['information']['data'][0]['data']['desc']))
        sheet.write(row, 2, str(i_set['information']['data'][0]['data']['plan']))
        sheet.write(row, 3, str(i_set['years']))
        row += 1
    workbook.save("保险数据.xls")
