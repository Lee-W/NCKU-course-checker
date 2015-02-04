import re
from html.parser import HTMLParser


class HTMLFormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.row_start, self.col_start = False, False
        self.table = list()

    def handle_data(self, data):
        if self.col_start is True:
            self.tmpColInOneRow += data

    def handle_starttag(self, tag, attrs):
        if tag == "tr" and not self.row_start:  # row start
            self.row_start = True

            self.tmpRow = list()
        elif tag in ("th", "td") and not self.col_start:  # col start
            # col start
            self.tmpColInOneRow = str()

            self.col_start = True

    def handle_endtag(self, tag):
        if tag == "tr" and self.row_start is True:  # row end
            self.row_start = False

            self.table.append(self.tmpRow)
        elif tag in ("th", "td") and self.col_start:  # col end
            self.tmpColInOneRow = re.sub("  *", " ",
                                         self.tmpColInOneRow.strip())
            self.tmpRow.append(self.tmpColInOneRow)

            self.col_start = False

    def get_header(self):
        return self.table[0]

    def get_content(self):
        return self.table[1:]

    def get_table(self):
        return self.table


if __name__ == '__main__':
    import urllib.request
    web = urllib.request.urlopen("http://lee-w.github.io/HTMLFormParser/")
    web_content = web.read().decode("utf8")
    web.close()

    parser = HTMLFormParser()
    for line in web_content.splitlines():
        parser.feed(line)
    print(parser.get_table())
