#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, build_opener, install_opener, HTTPCookieProcessor, HTTPHandler, urlopen
import cookielib
import urllib
from bs4 import BeautifulSoup
import sys
import re
import urlparse
import threading
import Queue
import time

reload(sys)
sys.setdefaultencoding('utf-8')

loginUrl = 'http://myns.cafe24.com/afterschool/regi/log/_login.php'
pageUrl = 'http://myns.cafe24.com/afterschool/main/main/gate.php'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
login_data = urllib.urlencode({'user_id' : '201710307', 'pass' : 'tkfkdgo1!', 'x' : '12', 'y' : '5', 'return_url' : '/afterschool/main/main/main.php'})
login_referer = 'http://myns.cafe24.com/afterschool/main/main/main.php'
join_head_url = 'http://myns.cafe24.com/afterschool/main/main/'
queue = Queue.Queue()


# Create a CookieJar Object to hold the cookies
cj = cookielib.CookieJar()
# Create an opener to open pages using the http protocol and to process cookies.
opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
# Commonly set User-Agent
opener.addheaders = [
        ('User-Agent', user_agent),
        ]
install_opener(opener)

def euc2utf(str):
        return unicode(str, 'euc-kr').encode('utf-8')

def utf2euc(str):
        return unicode(str, 'utf-8').encode('euc-kr')

def webLogin():
        loginReq = Request(loginUrl, login_data)
        loginReq.add_header('Referer', login_referer)

        loginResp = urlopen(loginReq)


        # page Crawl

        req = Request(pageUrl)
        response = urlopen(req)
        data = response.read()
        #print data
        return data

def fileLogin():
        f = open("./result.txt", 'r')
        data = f.read()
        f.close()
        return data

def woojooFileLogin():
        f = open("./woojoo.txt", 'r')
        data = f.read()
        f.close()
        return utf2euc(data)

def getParameter(url):
        parsed = urlparse.parse_qs(urlparse.urlparse(url).query)
        return parsed

def getWantedClass(soup):
        links = []
        links.append(soup.find(string=u'바이올린').find_parent('tr'))
        links.append(soup.find(string=re.compile(ur'바둑 A반', re.UNICODE)).find_parent('tr'))
        links.append(soup.find(string=re.compile(ur'장명숙 생명과학', re.UNICODE)).find_parent('tr'))
        return links

def joinClass(join_referer):
        joinUrl = 'http://myns.cafe24.com/afterschool/main/main/_blog_join.php'
        #joinUrl = 'http://ec2-13-124-44-54.ap-northeast-2.compute.amazonaws.com/cgi-bin/PostDump.cgi'

        #print join_referer
        #return
        parsed = getParameter(join_referer)

        join_data = urllib.urlencode({'club_no' : parsed['club_no'][0], 'div_no' : parsed['div_no'][0], 'member_no' : '11523', 'tque' : 'true'})

        joinReq = Request(joinUrl, join_data)
        joinReq.add_header('Referer', join_referer)

        joinResp = urlopen(joinReq)
        print '================================'
        print joinResp.read()




class ThreadUrl(threading.Thread):
        def __init__(self, queue):
                threading.Thread.__init__(self)
                self.queue = queue

        def run(self):
                while True:
                        url = self.queue.get()
                        joinClass(url)
                        self.queue.task_done()
                        print "url = " + url

start = time.time()

def getUrls():
        html = webLogin()
        #html = fileLogin()
        #html = woojooFileLogin()
        #print html
        print '================================'
        print 'login success'
        print '================================'

        soup = BeautifulSoup(html, 'lxml', from_encoding='euc-kr')
        # 해당하는 tr 을 찾는다
        for link in getWantedClass(soup):
                #print "link = " + str(link)
                img = link.find('a',  href=re.compile(r'blog_join.php'))
                #img = link.find('a',  href=re.compile(r'blog_main.php'))
                if img != None:
                        queue.put(join_head_url + img['href'])


def main():
        for i in range(3):
                t = ThreadUrl(queue)
                t.setDaemon(True)
                t.start()

        getUrls()

        queue.join()


main()
print "Elapsed Time: %s" % (time.time() - start)
