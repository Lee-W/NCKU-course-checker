from .parserHelper.HTMLFormParser import HTMLFormParser

import urllib.request

class NCKUcourseParser():
    def __init__(self):
        self.NCKUCourseCatalogURL = "http://140.116.165.74/qry/qry001.php?dept_no="
        self.URL = ""
        self.courseForm = []

    def setURL(self, dNo):
        self.URL = self.NCKUCourseCatalogURL + dNo

    def parseWebForm(self):
        web = urllib.request.urlopen(self.URL)
        webContent = web.read().decode("utf8")
        web.close()

        formParser = HTMLFormParser()
        for line in webContent.splitlines():
            formParser.feed(line)

        self.courseForm = formParser.getTable()

    def getCourseForm(self):
        return self.courseForm


if __name__ == '__main__':
    parser = NCKUcourseParser()
    parser.setURL('A1')
    parser.parseWebForm()
    print (parser.getCourseForm())
