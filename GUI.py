import NCKUcourseChecker
from tkinter import *


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(columnspan=500)
        self.createWidgets()
        self.checker = NCKUcourseChecker.NCKUcourseChecker()
        for i in range(len(self.checker.filterCondition)):
            e = Entry()
            e.grid(row=3, column=i)
            e.insert(END, "%s" % (self.checker.filterCondition[i]))


    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "系所代碼 ： "
        self.inputText.grid(row=0, column=0)
        self.inputText = Entry(self)
        self.inputText["width"] = 30
        self.inputText.grid(row=0, column=1, columnspan=6)

        self.search = Button(self)
        self.search["text"] = "搜尋"
        self.search.grid(row=1, column=0)
        self.search["command"] = self.searchMethod

        self.clear = Button(self)
        self.clear["text"] = "清除"
        self.clear.grid(row=2, column=0)
        # self.clear["command"] = self.clearMethod

    def searchMethod(self):
        self.checker.reset()
        departmentNo = self.inputText.get()
        self.checker.setDepartmentNo(departmentNo)
        self.checker.parseCourseData()
        self.checker.filterInfo()
        self.checker.sortedThroughtRemain()
        self.outputAsTable(self.checker.getFilteredTable()[1:])

    def clearMethod(self):
        pass


    def outputAsTable(self, table):
        for i in range(len(table)):
            for j in range(len(table[i])):
                e = Entry()
                e.grid(row=i+4, column=j)
                e.insert(END, "%s" % (table[i][j]))

if __name__ == '__main__':
    root = Tk()
    root.title("NCKU course checker")
    app = GUIChecker(master=root)
    app.mainloop()
