import NCKUcourseParser
import urllib.request
import sys

if __name__ == '__main__':
    URL = "http://140.116.165.74/qry/qry001.php?dept_no=AN"
    web = urllib.request.urlopen(URL)
    webContent = web.read().decode("utf8")
    web.close()

    parser = NCKUcourseParser.courseParser()
    for line in webContent.splitlines():
        parser.feed(line)

    for i in parser.courses:
        print (i)
        print ()
