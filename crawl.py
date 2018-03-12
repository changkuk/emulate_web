#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, build_opener, install_opener, HTTPCookieProcessor, HTTPHandler, urlopen
import cookielib
from bs4 import BeautifulSoup
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


initUrl = 'http://post.naver.com/async/my.nhn?memberNo=30910003&postListViewType=0&isExpertMy=true'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'

cj = cookielib.CookieJar()
opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
opener.addheaders = [
        ('User-Agent', user_agent),
        ]
install_opener(opener)

req = Request(initUrl)
response = urlopen(req)
data = json.loads(response.read(), encoding='utf-8')

print data
