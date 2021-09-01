#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import datetime
import urllib.request
import requests
import json
from bs4 import BeautifulSoup

host_url = "" #教务处链接
r = requests.get(
    url=host_url,
)
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.text, "lxml")


def getNowDate():
    now_time = datetime.datetime.now()
    yes_time = now_time+datetime.timedelta(days=-0)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time

def getTitle (soup):
    Title_links = soup.find('ul', {'class': 'tab-list'}).find('div', {'id': 'wp_news_w13'}).find_all('a')
    return Title_links

def getDate (soup):
    Date_links = soup.find('ul', {'class': 'tab-list'}).find('div', {'id': 'wp_news_w13'}).find_all('div')
    return Date_links

linklist_Title = getTitle(soup)
linklist_Date = getDate(soup)
contents = []
links = []
dates = []
send_data = ''
Now_Date = getNowDate()

for link in linklist_Title:
    contents.append(link.text.strip())
    links.append(link.get('href'))

for date in linklist_Date:
    dates.append(date.text.strip())

for date,text, link, in zip(dates, contents, links):
    _UrlLink = 'http://xxxx.xxx'+link+'\n' #教务处链接
    data = date+' '+text+':'+_UrlLink+''
    if date == Now_Date:
        send_data = send_data+data
def write():
    f = "/home/jwc_notice.txt" #自行更改文件保存路径
    _content = "今日教务处通知:\n\n"+send_data
    with open(f,"w", encoding="utf-8") as file:
        file.write(_content)
        print("成功写入!")


if __name__ == '__main__':
    print(send_data)
    if len(send_data) > 0:
      write()
