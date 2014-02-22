import NCKUcourseParser
import urllib.request
from operator import itemgetter


class NCKUcourseChecker():
    def __init__(self):
        self.filterCondition = ["系號", "序號", "課程名稱(連結課程地圖)", "學分", "教師姓名*:主負責老師", "餘額 ", "時間"]
        self.departmentNo = ""
        self.courseInfo = []
        self.filteredTable = []

    def setDepartmentNo(self, dNo):
        self.departmentNo = dNo

    def parseCourseData(self):
        URL = "http://140.116.165.74/qry/qry001.php?dept_no=" + self.departmentNo
        web = urllib.request.urlopen(URL)
        webContent = web.read().decode("utf8")
        web.close()

        parser = NCKUcourseParser.NCKUcourseParser()
        for line in webContent.splitlines():
            parser.feed(line)

        self.courseInfo = parser.getTable()

    def filterInfo(self):
        filteredIndex = []
        title = self.courseInfo[0]
        for i in range(len(title)):
            if title[i] in self.filterCondition:
                filteredIndex.append(i)

        self.filteredTable.append(self.filterCondition)
        for i in range(1, len(self.courseInfo)):
            self.filteredTable.append([self.courseInfo[i][j] for j in filteredIndex])

    def sortedThroughtRemainder(self, deleteZero=True):
        for i in self.filteredTable[1:]:
            i[5] = int(i[5])

        if deleteZero is True:
            self.filteredTable = list(filter(lambda x : x[5]!=0, self.filteredTable))
        self.filteredTable[1:] = sorted(self.filteredTable[1:], key=itemgetter(5), reverse=True)

    def getFilteredTable(self):
        return self.filteredTable

    def reset(self):
        self.departmentNo = ""
        self.courseInfo = []
        self.filteredTable = []
