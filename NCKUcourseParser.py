'''
enviroment : python 3.3.2
'''
from html.parser import HTMLParser


class courseParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.titleStart = False
        self.title = ""
        self.titles = []

        self.columnStart = False
        self.courseStart = False
        self.tmpText = ""
        self.courseInfo = []
        self.courses = []

    def handle_data(self, data):
        if self.titleStart is True:
            self.title += data
        elif self.titleStart is False and self.title != "":
            self.titles.append(self.title)
            self.title = ""

        if self.columnStart is True:
            if data == '額滿':
                self.tmpText = 0
            elif data.isdigit():
                self.tmpText = int(data)
            else:
                self.tmpText = data

    def handle_starttag(self, tag, attrs):
        if tag == "td" and self.columnStart is False and self.courseStart is True:
            self.columnStart = True
        elif tag == "th" and self.titleStart is False:
            self.titleStart = True
        elif tag == "tr" and self.courseStart is False and len(self.titles) > 0:
            self.courseStart = True

    def handle_endtag(self, tag):
        if tag == "td" and self.columnStart is True:
            self.columnStart = False
            self.courseInfo.append(self.tmpText)
            self.tmpText = ""
        elif tag == "th" and self.titleStart is True:
            self.titleStart = False
        elif tag == "tr" and self.courseStart is True:
            self.courseStart = False
            self.courses.append(self.courseInfo)
            self.courseInfo = []
