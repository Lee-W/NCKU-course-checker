from copy import deepcopy

from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Toplevel
from tkinter import Tk
from tkinter import ttk
from tkinter import font
from tkinter import Listbox
from tkinter import END
from tkinter import MULTIPLE

from NCKU_course_checker.NCKU_course_checker import NckuCourseChecker
from NCKU_course_checker.NCKU_course_parser import NoCourseAvailableError


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)
        self.createWidgets()

        self.all_columns = ["系號", "序號", "課程名稱(連結課程地圖)",
                            "餘額", "已選課人數", "教師姓名*:主負責老師",
                            "時間", "教室", "學分", "選必修", "限選條件",
                            "系所名稱", "年級", "組別", "類別", "班別",
                            "業界專家參與", "英語授課", "Moocs",
                            "跨領域學分學程", "備註",
                            "課程碼", "分班碼", "屬性碼"]
        self.default_choosen_filed = [True]*7 + [False]*17
        self.choosen_field = deepcopy(self.default_choosen_filed)

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

        self.setting = Button(self)
        self.setting["text"] = "欄位設定"
        self.setting.grid(row=1, column=4)
        self.setting["command"] = self.setting_method

        self.msg_text = Label(self)
        self.msg_text.grid(row=2, column=0)

    def setting_method(self):
        self.t = Toplevel(self)
        self.t.wm_title("Settings")
        self.create_column_checkbox(self.t)

    def create_column_checkbox(self, win):
        self.create_list_box()

        lb_label = Label(win)
        lb_label["text"] = "選擇欄位"
        lb_label.grid(row=1, column=0)

        confirm_btn = Button(win)
        confirm_btn["text"] = "確定"
        confirm_btn.grid(row=2, column=0)
        confirm_btn["command"] = self.choose_field

        default_btn = Button(win)
        default_btn["text"] = "回復預設值"
        default_btn.grid(row=2, column=1)
        default_btn["command"] = self.back_to_default_setting

    def back_to_default_setting(self):
        self.lb.grid_remove()
        self.choosen_field = self.default_choosen_filed
        self.create_list_box()

    def create_list_box(self):
        self.lb = Listbox(self.t, selectmode=MULTIPLE)
        for i in self.all_columns:
            self.lb.insert(END, i)
        for index, choosen in enumerate(self.choosen_field):
            if choosen:
                self.lb.select_set(index)

        self.lb.grid(row=1, column=1, sticky="nsew")

    def choose_field(self):
        self.choosen_field = [False]*len(self.all_columns)
        for choosen_index in self.lb.curselection():
            self.choosen_field[choosen_index] = True

        self.t.destroy()

    def searchMethod(self):
        departmentNo = self.inputText.get()
        self.checker = NckuCourseChecker(departmentNo)

        field = list()
        for index, choosen in enumerate(self.choosen_field):
            if choosen:
                field.append(self.all_columns[index])

        self.checker.field = field

        try:
            self.msg_text["text"] = "查詢中"
            self.outputAsTable()
            self.msg_text["text"] = ""
        except NoCourseAvailableError:
            self.msg_text["text"] = "沒有這個系所"
        except Exception:
            self.msg_text["text"] = "未知的錯誤"

    def clearMethod(self):
        try:
            self.tree.grid_remove()
        except Exception as e:
            print(e)

    def outputAsTable(self):
        title = self.checker.field
        courses = self.checker.get_courses(sort=True,
                                           delete_zero=True,
                                           descending=False)

        self.clearMethod()
        self.__set_up_tree_widget(title, courses)

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

    def __set_up_tree_widget(self, title, courses):
        self.tree = ttk.Treeview(columns=title, show="headings")
        vertial_scrollbar = ttk.Scrollbar(orient="vertical",
                                          command=self.tree.yview)
        horizontal_scrollbar = ttk.Scrollbar(orient="horizontal",
                                             command=self.tree.xview)
        self.tree.configure(yscrollcommand=vertial_scrollbar.set,
                            xscrollcommand=horizontal_scrollbar.set)
        self.tree.grid(row=3, column=0)
        vertial_scrollbar.grid(row=3, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=4, column=0, sticky="we")


if __name__ == '__main__':
    root = Tk()
    root.title("NCKU course checker")
    root.resizable(0, 0)
    app = GUIChecker(master=root)
    app.mainloop()
