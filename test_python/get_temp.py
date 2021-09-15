# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 11:20:40 2018
@author: CSM
"""
import csv
import time

import requests
from bs4 import BeautifulSoup

user_agent = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}


# 参数city为城市拼音,*years为年份参数（int类型）,若只传入一个数字则只爬取对应年份数据,若输入多个年份则默认以第一个年份为起始年,最后一个年份为终止年（例如传入2011,2018，则爬取2011到2018年天气数据），目前最久远的天气数据只有2011年的
def get_weather_historic_data(city, *years):
    res = []
    file = open('temp.csv', 'w', encoding='utf_8_sig')
    cw = csv.writer(file)
    dataArray = []
    for year in range(years[0], years[-1] + 1):
        print('正在获取%d年数据...' % (year))
        for month in range(1, 13):
            if month < 10:
                response = requests.get('http://lishi.tianqi.com/%s/%d0%d.html' % (city, year, month),
                                        headers=user_agent).text
            else:
                response = requests.get('http://lishi.tianqi.com/%s/%d%d.html' % (city, year, month),
                                        headers=user_agent).text
            soup = BeautifulSoup(response, "html.parser")
            # 检查是否找到该时段天气数据，没有则跳到下个月
            try:
                ul = soup.find('div', class_='tian_three').find_all('ul')
            except BaseException as ex:
                continue
            # columns作为DataFrame对象的列名
            columns = ul[0].get_text().split()
            # 每7个输出一行
            j = 0
            itemArray = [0] * 7
            for item in columns:
                if item == 'item':
                    break
                if j == 2 or j == 3:
                    itemArray[j] = item[:len(item) - 1]
                else:
                    itemArray[j] = item
                j = j + 1
                if j > 6:
                    j = 0
                    cw.writerow(itemArray)


st = time.time()
# shenzhen指的是深圳，2011是起始年份，2018是终止年份，即爬取2011到2018年深圳天气数据
get_weather_historic_data('shenzhen', 2019, 2020)
print('完成,用时', round(time.time() - st, 3), 's')
