'''
enviroment : python 3.3.2
'''
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import urllib.request
import sys

class courseParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.titleStart = False
        self.columnStart = False
        self.courseStart =False
        self.title = ""
        self.titles = []
        self.courseInfo = []
        self.courses = []

    def handle_data(self, data):
        if self.titleStart == True:
            self.title += data
        elif self.titleStart == False and self.title!="":
            self.titles.append(self.title)
            self.title = ""

        if self.courseStart == True:
            self.courseInfo.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == "th" and self.titleStart == False:
            self.titleStart = True

        if tag == "tr" and self.courseStart == False and len(self.titles) > 0:
            self.courseStart = True

        if tag == "td" and self.columnStart == False:
            self.columnStart = True

    def handle_endtag(self, tag):
        if tag == "th" and self.titleStart == True:
            self.titleStart = False

        if tag == "tr" and self.courseStart == True:
            self.courses.append(self.courseInfo)
            self.courseInfo = []
            self.courseStart = False

        if tag == "td" and self.courseStart == True:
            self.columnStart = False



if __name__ == '__main__':
    URL = "http://140.116.165.74/qry/qry001.php?dept_no=AN"
    web = urllib.request.urlopen(URL)
    webContent = web.read().decode("utf8")
    web.close()

    parser = courseParser()
    for line in webContent.splitlines():
        parser.feed(line)

    for i in parser.courses:
        print (i)
        print ()
