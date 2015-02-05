from copy import deepcopy

from tkinter import Tk
from tkinter import ttk
from tkinter import font
from tkinter import Frame
from tkinter import Toplevel
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Entry
from tkinter import Label
from tkinter import Listbox
from tkinter import BooleanVar
from tkinter import MULTIPLE
from tkinter import END

from NCKU_course_checker.NCKU_course_checker import NckuCourseChecker
from NCKU_course_checker.NCKU_course_parser import NoCourseAvailableError


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)

        self.__set_default_value()
        self.__create_widgets()

    def __set_default_value(self):
        self.all_field = ["系號", "序號", "課程名稱(連結課程地圖)", "餘額", "已選課人數",
                          "教師姓名*:主負責老師", "時間", "教室", "學分", "選必修", "限選條件",
                          "系所名稱", "年級", "組別", "類別", "班別",
                          "業界專家參與", "英語授課", "Moocs", "跨領域學分學程", "備註",
                          "課程碼", "分班碼", "屬性碼"]
        self.default_choosen_field = [True]*7 + [False]*17
        self.choosen_field = deepcopy(self.default_choosen_field)

        self.sort_var = BooleanVar()
        self.dz_var = BooleanVar()
        self.sort_var.set(True)
        self.dz_var.set(True)

    def __create_widgets(self):
        self.input_label = Label(self, text="系所代碼 ： ")
        self.input_field = Entry(self, width=30)
        self.search_btn = Button(self, text="搜尋", command=self.__search_method)
        self.clear_btn = Button(self, text="清除", command=self.__clear_method)
        self.setting_btn = Button(self, text="設定", command=self.__setting_method)
        self.msg_text = Label(self)

        self.input_label.grid(row=0, column=0)
        self.input_field.grid(row=0, column=1, columnspan=6)
        self.search_btn.grid(row=1, column=0)
        self.clear_btn.grid(row=1, column=2)
        self.setting_btn.grid(row=1, column=4)
        self.msg_text.grid(row=2, column=0)

    def __search_method(self):
        department_no = self.input_field.get()
        self.checker = NckuCourseChecker(department_no)

        field = list()
        for index, choosen in enumerate(self.choosen_field):
            if choosen:
                field.append(self.all_field[index])
        self.checker.field = field

        try:
            self.msg_text["text"] = "查詢中"
            self.__output_as_table()
            self.msg_text["text"] = ""
        except NoCourseAvailableError:
            self.msg_text["text"] = "沒有這個系所"
        except Exception:
            self.msg_text["text"] = "未知的錯誤"

    def __output_as_table(self):
        title = self.checker.field
        courses = self.checker.get_courses(sort=self.sort_var.get(),
                                           delete_zero=self.dz_var.get(),
                                           descending=False)

        self.__clear_method()
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

    def __clear_method(self):
        try:
            self.__remove_tree_widget()
        except Exception as e:
            print("Widget not yet create. Not an error", e)

    def __remove_tree_widget(self):
        self.tree_vsb.grid_remove()
        self.tree_hsb.grid_remove()
        self.tree.grid_remove()

    def __set_up_tree_widget(self, title, courses):
        self.tree = ttk.Treeview(columns=title, show="headings", height=len(courses))
        self.tree_vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree_hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_vsb.set, xscrollcommand=self.tree_hsb.set)

        self.tree.grid(row=3, column=0)
        self.tree_vsb.grid(row=3, column=1, sticky="ns")
        self.tree_hsb.grid(row=4, column=0, sticky="we")

    def __setting_method(self):
        self.setting_win = Toplevel(self)
        self.setting_win.wm_title("Settings")
        self.__create_setting_win_widget()

    def __create_setting_win_widget(self):
        choose_field_label = Label(self.setting_win, text="選擇欄位")
        self.__create_choose_field_listbox()
        self.sort_cb = Checkbutton(self.setting_win, text="根據課程餘額排序",
                                   variable=self.sort_var)
        self.delete_zero_cb = Checkbutton(self.setting_win, text="排除沒餘額的課程",
                                          variable=self.dz_var)
        confirm_btn = Button(self.setting_win, text="確定", command=self.__confirm_setting)
        default_btn = Button(self.setting_win, text="回復預設值", command=self.__restore_setting)

        choose_field_label.grid(row=1, column=0)
        self.delete_zero_cb.grid(row=2, column=0)
        self.sort_cb.grid(row=3, column=0)
        confirm_btn.grid(row=4, column=0)
        default_btn.grid(row=4, column=1)

    def __create_choose_field_listbox(self):
        self.choose_field_listbox = Listbox(self.setting_win,
                                            selectmode=MULTIPLE,
                                            height=len(self.all_field))
        for i in self.all_field:
            self.choose_field_listbox.insert(END, i)
        for index, choosen in enumerate(self.choosen_field):
            if choosen:
                self.choose_field_listbox.select_set(index)

        self.choose_field_listbox.grid(row=1, column=1, sticky="nsew")

    def __confirm_setting(self):
        self.choosen_field = [False]*len(self.all_field)
        for choosen_index in self.choose_field_listbox.curselection():
            self.choosen_field[choosen_index] = True

        self.setting_win.destroy()

    def __restore_setting(self):
        self.choose_field_listbox.grid_remove()
        self.choosen_field = self.default_choosen_field
        self.__create_choose_field_listbox()

        self.sort_var.set(True)
        self.dz_var.set(True)


if __name__ == '__main__':
    root = Tk()
    root.title("NCKU course checker")
    root.resizable(0, 0)
    app = GUIChecker(master=root)
    app.mainloop()
