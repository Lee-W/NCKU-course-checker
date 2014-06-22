from html.parser import HTMLParser


class HTMLFormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rowStart = False
        self.columnStart = False
        self.tmpColInOneRow = []
        self.tmpRow = []
        self.table = []

    def handle_data(self, data):
        if self.columnStart is True:
            self.tmpColInOneRow.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == "tr" and self.rowStart is False:
            self.rowStart = True
        elif tag == "th" or tag == "td" and self.columnStart is False:
            self.columnStart = True

    def handle_endtag(self, tag):
        if tag == "tr" and self.rowStart is True:
            self.rowStart = False
            self.table.append(self.tmpRow)
            self.tmpRow = []
        elif tag == "th" or tag == "td" and self.columnStart is True:
            self.columnStart = False
            self.tmpRow.append("".join(self.tmpColInOneRow))
            self.tmpColInOneRow = []

    def getHeader(self):
        return self.table[0]

    def getContent(self):
        return self.table[1:]

    def getTable(self):
        return self.table


if __name__ == '__main__':
    import requests
    url = "http://lee-w.github.io/HTMLFormParser/"
    req = requests.get(url)
    webContent = req.text

    parser = HTMLFormParser()
    for line in webContent.splitlines():
        parser.feed(line)
    print (parser.getTable())
