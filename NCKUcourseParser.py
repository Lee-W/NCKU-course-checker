'''
enviroment : python 3.3.2
'''
from HTMLFormParser import HTMLFormParser


class NCKUcourseParser(HTMLFormParser):
    def handle_data(self, data):
        if self.columnStart is True:
            if data == '額滿':
                self.tmpColInOneRow = ['0']
            else:
                self.tmpColInOneRow.append(data)

if __name__ == '__main__':
    import urllib.request
    web = urllib.request.urlopen("http://140.116.165.74/qry/qry001.php?dept_no=AN")
    webContent = web.read().decode("utf8")
    web.close()

    parser = NCKUcourseParser()
    for line in webContent.splitlines():
        parser.feed(line)
    print (parser.getTable())
