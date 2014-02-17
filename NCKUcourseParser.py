'''
enviroment : python 3.3.2
'''
from html.parser import HTMLParser


class courseParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rowStart = False
        self.columnStart = False
        self.tmpColInOneRow = []
        self.tmpRow = []
        self.table = []

    def handle_data(self, data):
        if self.columnStart is True:
            if data == '額滿':
                self.tmpColInOneRow = [0]
            elif data.isdigit():
                self.tmpColInOneRow.append(int(data))
            else:
                self.tmpColInOneRow.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == "tr" and self.rowStart is False:
            self.rowStart = True
        elif tag == "th" and self.columnStart is False:
            self.columnStart = True
        elif tag == "td" and self.columnStart is False:
            self.columnStart = True

    def handle_endtag(self, tag):
        if tag == "tr" and self.rowStart is True:
            self.rowStart = False
            self.table.append(self.tmpRow)
            self.tmpRow = []
        elif tag == "th" and self.columnStart is True:
            self.columnStart = False
            self.tmpRow.append(self.tmpColInOneRow)
            self.tmpColInOneRow = []
        elif tag == "td" and self.columnStart is True:
            self.columnStart = False
            self.tmpRow.append(self.tmpColInOneRow)
            self.tmpColInOneRow = []

    def getTitle(self):
        return self.table[0]

    def getContent(self):
        return self.table[1:]

    def getTable(self):
        return self.table


if __name__ == '__main__':
    import urllib.request
    web = urllib.request.urlopen("http://140.116.165.74/qry/qry001.php?dept_no=AN")
    webContent = web.read().decode("utf8")
    web.close()

    parser = courseParser()
    for line in webContent.splitlines():
        parser.feed(line)
    print (parser.getTitle())
    for i in parser.getContent():
        print (parser.getContent())
        print ()
