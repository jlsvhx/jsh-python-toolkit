# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:14:41 2022

@author: jshfs
"""
import urllib
from urllib import request, parse
from http import cookiejar



url = r'https://xkkm.sdzk.cn/xkkm/queryXxInfor'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=EB903013CB6B29BAEAEB12E7CF469738; PTGK-PT=33624574; JSESSIONID=EB903013CB6B29BAEAEB12E7CF469738',
    'Host': r'xkkm.sdzk.cn',
    'Origin': r'https://xkkm.sdzk.cn',
    'Referer': r'https://xkkm.sdzk.cn/web/xx.html',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
cookie = cookiejar.CookieJar()
cookies = urllib.request.http



with open('F:\学校代号及编码.txt', 'r') as f:
    list1 = f.readlines()

for i in range(0, len(list1)):
    list1[i] = list1[i].rstrip('\n')
#print(list1)

for i in range(0,len(list1),2):
    print(list1[i]+list1[i+1])
    
    test = {
            'dm':list1[i],
            'mc':list1[i+1],
            'yzm':'ok'
            }
    test = parse.urlencode(test).encode('utf-8')
    #print(test)
    req = request.Request(url, headers=headers, data=test)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    prefix = r'F:\\'
    with open(prefix+list1[i]+'.txt', 'a',encoding='utf-8') as f:
      f.write(page)
    #print(page)

