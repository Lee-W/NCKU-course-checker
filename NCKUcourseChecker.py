import NCKUcourseParser
import urllib.request
from operator import itemgetter
from tkinter import *
# from tabulate import tabulate


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(columnspan=20)
        self.createWidgets()
        self.filterCondition = ["系號", "序號", "課程名稱(連結課程地圖)", "學分", "教師姓名*:主負責老師", "餘額 ", "時間"]

    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "系所代碼 ： "
        self.inputText.grid(row=0, column=0)
        self.inputText = Entry(self)
        self.inputText["width"] = 10
        self.inputText.grid(row=0, column=1, columnspan=6)

        self.search = Button(self)
        self.search["text"] = "搜尋"
        self.search.grid(row=1, column=0)
        self.search["command"] = self.searchMethod

        self.clear = Button(self)
        self.clear["text"] = "清除"
        self.clear.grid(row=2, column=0)

    def searchMethod(self):
        departmentNo = self.inputText.get()

        URL = "http://140.116.165.74/qry/qry001.php?dept_no=" + departmentNo
        web = urllib.request.urlopen(URL)
        webContent = web.read().decode("utf8")
        web.close()

        parser = NCKUcourseParser.courseParser()
        for line in webContent.splitlines():
            parser.feed(line)

        filteredIndex = []
        title = parser.getTitle()
        for i in range(len(title)):
            if title[i] in self.filterCondition:
                filteredIndex.append(i)

        filteredCourseInfo = []
        for i in range(len(parser.getContent())):
            if parser.getContent()[i][15] > '0':
                filteredCourseInfo.append([parser.getContent()[i][j] for j in filteredIndex])

        filteredCourseInfo = sorted(filteredCourseInfo, key=itemgetter(3), reverse=True)

        self.outputAsTable(filteredCourseInfo)

    def outputAsTable(self, table):
        for i in range(len(table)):
            for j in range(len(table[i])):
                e = Entry()
                e.grid(row=i, column=j)
                e.insert(END, "%s"%(table[i][j]))

if __name__ == '__main__':
#     filterCondition = ["系號", "序號", "課程名稱(連結課程地圖)",  "餘額 ", "時間"]
#
#
#     # formatStr = "{0:2}\t{1:3}\t{2:25s}\t{3}\t{4}"
#     # for i in filteredCourseInfo:
#         # print (formatStr.format(*i))
#
    root = Tk()
    root.title("NCKU course checker")
    app = GUIChecker(master=root)
    app.mainloop()
#
#     outputAsTable(filteredCourseInfo)
#     mainloop()
#
