import logging
from copy import deepcopy

from tkinter import Tk, ttk, font
from tkinter import Frame, Toplevel
from tkinter import Button, Entry, Label, Listbox
from tkinter import MULTIPLE, END

from nckucourseparser.nckucoursecrawler import NckuCourseCrawler
from nckucourseparser.nckucourseparser import NckuCourseParser
from nckucourseparser.nckucourseparser import NoCourseAvailableError


class GUIChecker(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(columnspan=2000)

        self.__set_default_value()
        self.__create_widgets()
        self.__locate_widges()

        self.setting_on = False

    def __set_default_value(self):
        self.ALL_FIELDS = ["系號", "序號", "餘額", "課程名稱(連結課程地圖)",
                           "學分", "時間", "教師姓名*:主負責老師"
                           "已選課人數", "教室", "選必修", "限選條件",
                           "系所名稱", "年級", "組別", "類別", "班別",
                           "業界專家參與", "英語授課", "Moocs", "跨領域學分學程",
                           "備註", "課程碼", "分班碼", "屬性碼"]
        self.default_choosen_field = ["系號", "序號", "餘額", "課程名稱(連結課程地圖)",
                                      "學分", "時間", "教師姓名*:主負責老師"]
        self.choosen_field = deepcopy(self.default_choosen_field)

    def __create_widgets(self):
        self.input_label = Label(self, text="系所代碼 ： ")
        self.input_field = Entry(self, width=30)
        self.search_btn = Button(self, text="搜尋", command=self.__search_method)
        self.clear_btn = Button(self, text="清除", command=self.__clear_method)
        self.setting_btn = Button(self, text="設定", command=self.__setting_method)
        self.msg_text = Label(self)

    def __locate_widges(self):
        self.input_label.grid(row=0, column=0)
        self.input_field.grid(row=0, column=1, columnspan=6)
        self.search_btn.grid(row=1, column=0)
        self.clear_btn.grid(row=1, column=2)
        self.setting_btn.grid(row=1, column=4)
        self.msg_text.grid(row=2, column=0)

    def __search_method(self):
        department_no = self.input_field.get()
        self.msg_text['text'] = '查詢中'
        try:
            self.__attach_course_table(department_no)
        except NoCourseAvailableError as e:
            logging.debug(e)
            self.msg_text['text'] = '沒有這個系所'
        except Exception as e:
            logging.exception('Seach Method: ')
            self.msg_text['text'] = '未知的錯誤'
        else:
            self.msg_text['text'] = ''

    def __attach_course_table(self, dept_no):
        courses = self.__search_courses(dept_no)
        title = list(courses.columns.values)

        self.__clear_method()
        self.__set_up_tree_widget(title, len(courses))

        for field in title:
            self.tree.heading(field, text=field)
            self.tree.column(field, width=font.Font().measure(field))

        for index, course in courses.iterrows():
            self.tree.insert('', 'end', values=tuple(course.values))
            for ix, val in enumerate(course.values):
                col_w = font.Font().measure(val) + 10
                if self.tree.column(title[ix], width=None) < col_w:
                    self.tree.column(title[ix], width=col_w)

    def __search_courses(self, dept_no):
        crawler = NckuCourseCrawler(dept_no=dept_no)
        html = crawler.get_raw_HTML()
        parser = NckuCourseParser(html)
        parser.include_fields = self.choosen_field
        logging.info("Choosen Field: {}".format(self.choosen_field))
        courses = parser.parse(sort=True)
        print(courses)
        courses['餘額'] = courses['餘額'].apply(int)
        return courses

    def __clear_method(self):
        try:
            self.__remove_tree_widget()
        except Exception as e:
            logging.debug(
                'Widget not yet created. Not and Error. {}'.format(e)
            )

    def __remove_tree_widget(self):
        self.tree_vsb.grid_remove()
        self.tree_hsb.grid_remove()
        self.tree.grid_remove()

    def __set_up_tree_widget(self, title, courses_num):
        tree_height = min(30, courses_num)
        self.tree = ttk.Treeview(columns=title, show="headings",
                                 height=tree_height)
        self.tree_vsb = ttk.Scrollbar(orient="vertical",
                                      command=self.tree.yview)
        self.tree_hsb = ttk.Scrollbar(orient="horizontal",
                                      command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_vsb.set,
                            xscrollcommand=self.tree_hsb.set)

        self.tree.grid(row=3, column=0)
        self.tree_vsb.grid(row=3, column=1, sticky="ns")
        self.tree_hsb.grid(row=4, column=0, sticky="we")

    def __setting_method(self):
        if not self.setting_on:
            self.setting_on = True

            self.setting_win = Toplevel(self)
            self.setting_win.wm_title("Settings")
            self.__create_setting_win_widget()

    def __create_setting_win_widget(self):
        choose_field_label = Label(self.setting_win, text="選擇欄位")
        self.__create_choose_field_listbox()
        confirm_btn = Button(self.setting_win, text="確定", command=self.__confirm_setting)
        default_btn = Button(self.setting_win, text="回復預設值", command=self.__restore_setting)

        confirm_btn.grid(row=0, column=0)
        default_btn.grid(row=0, column=1)
        choose_field_label.grid(row=1, column=0)

    def __create_choose_field_listbox(self):
        self.choose_field_listbox = Listbox(self.setting_win,
                                            selectmode=MULTIPLE,
                                            height=len(self.ALL_FIELDS))
        for i in self.ALL_FIELDS:
            self.choose_field_listbox.insert(END, i)
        for index, choosen in enumerate(self.choosen_field):
            if choosen:
                self.choose_field_listbox.select_set(index)

        self.choose_field_listbox.grid(row=1, column=1, sticky="nsew")

    def __confirm_setting(self):
        print(self.choose_field_listbox)
        print(self.choose_field_listbox.curselection())
        selections = self.choose_field_listbox.curselection()
        self.choosen_field = [
            self.ALL_FIELDS[col_index] for col_index in selections
        ]
        self.setting_win.withdraw()
        self.setting_on = False

    def __restore_setting(self):
        self.choose_field_listbox.grid_remove()
        self.choosen_field = self.default_choosen_field
        self.__create_choose_field_listbox()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    root = Tk()
    root.title("NCKU course checker")
    root.resizable(0, 0)
    app = GUIChecker(master=root)
    app.mainloop()
