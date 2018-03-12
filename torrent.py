#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, HTTPHandler, HTTPCookieProcessor, urlopen, build_opener, install_opener
from bs4 import BeautifulSoup
from base64 import b64encode
import cookielib
import sys
import re
import transmissionrpc

reload(sys)
sys.setdefaultencoding('utf-8')

startUrl = 'https://torrentkim10.net'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
startFileName = './torrent.html'
mp3PageFileName = './101273.html'

torrentServer = '221.150.182.23'
torrentPort = 9091
torrentUser = 'admin'
torrentPassword = 'lgtwins'

flagFile = False

# Create a CookieJar Object to hold the cookies
cj = cookielib.CookieJar()
# Create an opener to open pages using the http protocol and to process cookies.
opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
# Commonly set User-Agent
opener.addheaders = [
        ('User-Agent', user_agent),
        ]
install_opener(opener)


def getPage(url, referer=None):
        req = Request(url)
        if referer:
                req.add_header('Referer', referer)
        data = urlopen(req).read()
        return data

def getPageFromFile(filename):
        f = open(filename, 'r')
        data = f.read()
        f.close()
        return data

def getMP3PageUrl(html):
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', style='line-height:160%')
        li = div.find('li', string=re.compile(ur'멜론.*Top100'))
        return startUrl + li.contents[0]['href']

def getDownLoadUrl(html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', id='file_table')
        tag = table.find('a', href=re.compile(r'/bbs/download.php?'))
        return startUrl + tag['href']

def main():
        if flagFile == True:
                html = getPageFromFile(startFileName)
        else:
                html = getPage(startUrl)

        mp3PageUrl = getMP3PageUrl(html)

        if flagFile == True:
                html = getPageFromFile(mp3PageFileName)
        else:
                html = getPage(mp3PageUrl)

        downloadUrl = getDownLoadUrl(html)
        torrent = getPage(downloadUrl, mp3PageUrl)
        print "downloadURL = " + downloadUrl
        print "refererURL = " + mp3PageUrl

        tc = transmissionrpc.Client(torrentServer, torrentPort, torrentUser, torrentPassword)
        torrents = tc.get_torrents()
        #for torrent in torrents:
                #if (torrent.status == 'seeding'):
                        #tc.remove_torrent(torrent.id)

        tc.add_torrent(b64encode(torrent))
main()
