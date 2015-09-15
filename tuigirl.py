#coding:utf-8
__author__ = 'ColdCodeCool'

import urllib2
import re
import urllib
import os

class Tuigirl:
    #页面初始化
    def __init__(self):
        self.URL = 'http://www.lsm.me/forum.php?mod=forumdisplay&fid=39&sortid=1&sortid=1&page='
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
        self.PageIndex = 1

    #获取索引页面内容
    def GetPage(self,PageIndex):
        url = self.URL + str(PageIndex)
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    #获取索引页面所有MM的信息，list格式
    def GetInfo(self, PageIndex):
        page = self.GetPage(PageIndex)
        pattern1 = re.compile(r'<a class="pic" target="_blank" href="(.*?)".*?alt="(.*?)"', re.S)
        items = re.findall(pattern1, page)
        return items

    def GetDetailPage(self, detailURL):
        response = urllib2.urlopen(detailURL)
        return response.read()

    def GetImgs(self, detailPage):
        pattern = re.compile('<li>.*?<img.*?src="(.*?)"',re.S)
        images = re.findall(pattern, detailPage)
        return images


    def Saveimgs(self, images, name):
        number = 1
        for imageURL in images:
            SplitPath = imageURL.split('.')
            if len(SplitPath) > 3:
                Filetail = 'jpg'
                filename = name + '/' + str(number) + '.' + Filetail
                self.SaveImg(imageURL, filename)
                number += 1

    def SaveImg(self, imageURL, filename):
        image = urllib.urlopen(imageURL)
        data = image.read()
        file = open(filename, 'wb')
        file.write(data)
        print u"正在保存", filename
        file.close()

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print "创建名字叫做", path, "的文件夹"
            os.makedirs(path)
            return True
        else:
            return False

    def SavePageInfo(self,PageIndex):
        #获取第一页MM列表
        contents = self.GetInfo(PageIndex)
        for item in contents:
            #item[0]个人URL，item[1]姓名编号
            DetailURL = str("http://www.lsm.me/") + item[0]
            urls = item[0].split('-')
            #获取MM名字,注意对中文字符编码的处理
            name = item[1].split()[3].decode('utf-8')
            #获取页面详细代码
            DetailPage = self.GetDetailPage(DetailURL)
            #获取个人页面中所有图片列表
            images = self.GetImgs(DetailPage)
            self.mkdir(name)
            #保存个人图片
            self.Saveimgs(images, name)

    def SavePagesInfo(self, start, end):
        for i in range(start, end+1):
            self.SavePageInfo(i)

tuigirl = Tuigirl()
tuigirl.SavePagesInfo(1, 2)
