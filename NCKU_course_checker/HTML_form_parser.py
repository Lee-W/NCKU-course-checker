import re
from html.parser import HTMLParser


class HTMLFormParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.row_start, self.col_start = False, False
        self.tables = list()

    def handle_data(self, data):
        if self.col_start is True:
            self.tmpColInOneRow += data

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.current_table = list()
        elif tag == "tr" and not self.row_start:  # row start
            self.row_start = True

            self.tmpRow = list()
        elif tag in ("th", "td") and not self.col_start:  # col start
            # col start
            self.tmpColInOneRow = str()

            self.col_start = True

    def handle_endtag(self, tag):
        if tag == "table":
            self.tables.append(self.current_table)
        elif tag == "tr" and self.row_start is True:  # row end
            self.row_start = False

            self.current_table.append(self.tmpRow)
        elif tag in ("th", "td") and self.col_start:  # col end
            self.tmpColInOneRow = re.sub("  *", " ",
                                         self.tmpColInOneRow.strip())
            self.tmpRow.append(self.tmpColInOneRow)

            self.col_start = False

    def get_header(self):
        if self.get_number_of_tables() == 1:
            return self.tables[0][0]
        else:
            return [table[0] for table in self.tables]

    def get_content(self):
        if self.get_number_of_tables() == 1:
            return self.tables[0][1:]
        else:
            return [table[1:] for table in self.tables]

    def get_tables(self):
        if self.get_number_of_tables() == 1:
            return self.tables[0]
        return self.tables

    def get_number_of_tables(self):
        return len(self.tables)


if __name__ == '__main__':
    # import urllib.request
    # web = urllib.request.urlopen("http://lee-w.github.io/HTMLFormParser/")
    # web_content = web.read().decode("utf8")
    # web.close()

    with open("./sample/sample_html.html") as f:
        web_content = f.read()

    parser = HTMLFormParser()
    for line in web_content.splitlines():
        parser.feed(line)
    print(parser.get_header())
    print(parser.get_content())
    print(parser.get_number_of_tables())
    print(parser.get_tables())
