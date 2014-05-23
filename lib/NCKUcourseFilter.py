import urllib.request
from operator import itemgetter


class NCKUcourseFilter():
    def __init__(self):
        self.defaultFilter = ["系號", "序號", "課程名稱(連結課程地圖)", "學分", "教師姓名*:主負責老師", "餘額 ", "時間"]
        self.filterCondition = self.defaultFilter

        self.courseData = []
        self.filteredData = []

    def setCourseData(self, data):
        self.courseData = self.formatData(data)

    def setFilterCondition(self):
        '''not yet finished'''
        pass

    def formatData(self, table):
        for row in range(len(table)):
            for col in range(len(table[row])):
                if table[row][col] == '額滿':
                    table[row][col] = '0'
        return table

    def filterInfo(self):
        filteredIndex = []

        title = self.courseData[0]
        for i in range(len(title)):
            if title[i] in self.filterCondition:
                filteredIndex.append(i)

        self.filteredData.append(self.filterCondition)
        for i in range(1, len(self.courseData)):
            self.filteredData.append([self.courseData[i][j] for j in filteredIndex])


    def sortData(self, sortCondition='餘額 ', assending=True, deleteZero=True):
        sortIndex = 0
        for i in range(len(self.filteredData[0])):
            if (self.filteredData[0][i] == sortCondition):
                sortIndex = i
                break

        for row in range(1, len(self.filteredData)):
            for col in range(len(self.filteredData[row])):
                if (self.filteredData[row][col].isdigit()):
                    self.filteredData[row][col] = int(self.filteredData[row][col])

        if deleteZero is True:
            self.filteredData = list(filter(lambda x : x[sortIndex]!=0, self.filteredData))

        self.filteredData[1:] = sorted(self.filteredData[1:], key=itemgetter(sortIndex), reverse=assending)

    def getFilteredData(self):
        return self.filteredData

    def reset(self):
        self.courseData = []
        self.filteredData = []
        self.filterCondition = self.defaultFilter
