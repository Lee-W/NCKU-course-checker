from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Tk
from tkinter import ttk
from tkinter import font

from NCKU_course_checker.NCKU_course_checker import NckuCourseChecker


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(columnspan=2000)
        self.createWidgets()

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
        self.clear.grid(row=1, column=2)
        self.clear["command"] = self.clearMethod

    def searchMethod(self):
        departmentNo = self.inputText.get()
        self.checker = NckuCourseChecker(departmentNo)
        self.outputAsTable()

    def clearMethod(self):
        self.tree.delete(*self.tree.get_children())

    def outputAsTable(self):
        title = self.checker.field
        courses = self.checker.get_courses()

        self.tree = ttk.Treeview(columns=title, show="headings")
        self.tree.grid(row=2, column=0)

        for field in title:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=font.Font().measure(field))

        course_tuples = list()
        for course in courses:
            tmp_tuple = tuple()
            for field in title:
                tmp_tuple = tmp_tuple + tuple([course[field]])
            course_tuples.append(tmp_tuple)

        for course in course_tuples:
            self.tree.insert('', 'end', values=course)
            for ix, val in enumerate(course):
                col_w = font.Font().measure(val) + 10
                if self.tree.column(title[ix], width=None) < col_w:
                    self.tree.column(title[ix], width=col_w)

        # for index_i, course in enumerate(courses):
        #     for index_j, field in enumerate(title):
        #         e = Entry()
        #         e.grid(row=index_i+4, column=index_j)
        #         e.insert(END, "%s" % (course[field]))


if __name__ == '__main__':
    root = Tk()
    root.title("NCKU course checker")
    app = GUIChecker(master=root)
    app.mainloop()
