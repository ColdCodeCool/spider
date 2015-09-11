# coding=utf-8
__author__ = 'liyang'

import urllib2
import re
#I am a stockbroker

class StockBroker:
    def __init__(self):
        self.siteURL = "http://quote.eastmoney.com/sh600415.html"
        self.headers = {'Referer': 'http://same.eastmoney.com/s?z=eastmoney&c=175&op=1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' +
                                     '(KHTML,like Gecko) Chrome/45.0.2454.85 Safari/537.36',
                        'X-Requested-With':'ShockwaveFlash/18.0.0.232'
                        }

    def getHtml(self):
        request = urllib2.Request(self.siteURL, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    def getContents(self):
        pattern = re.compile(r'<div.*?bt oh">.*?red">(.+?)</span>', re.DOTALL)
        item = re.findall(pattern, self.getHtml())
        print item[0]

stockbroker = StockBroker()
stockbroker.getContents()
print stockbroker.getHtml()