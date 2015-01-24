import json
import os

from .lib.NCKU_course_crawler import NckuCourseCrawler
from .lib.HTML_form_parser import HTMLFormParser


class NckuCourseParser(NckuCourseCrawler):
    def __init__(self, dept_no, year="", semester=""):
        super().__init__(year=year, semester=semester, dept_no=dept_no)
        self.field, self.exclude = list(), list()

    def __parse(self):
        form_parser = HTMLFormParser()
        for line in super().get_raw_HTML().splitlines():
            form_parser.feed(line)

        self.title = form_parser.get_header()
        self.contents = form_parser.get_content()

    def set_field(self, field):
        # reset exclude
        self.exclude = list()

        self.field = field

    def set_exclude(self, exclude):
        # reset field
        self.field = self.title

        self.exclude = exclude

    def get_courses(self):
        self.__parse()
        print(self.get_URL())

        if self.contents == [["查無課程資訊"]]:
            raise NoCourseAvailableError("No course available")

        if not self.field:
            self.field = self.title

        courses = list()
        for content in self.contents:
            course = dict(zip(self.title, content))
            if content == self.title:
                continue

            if self.exclude:
                course = {key: value for (key, value) in course.items()
                          if key not in self.exclude}
            else:
                course = {key: value for (key, value) in course.items()
                          if key in self.field}

            courses.append(course)
        return courses

    def set_expor_path(self, path):
        self.path = path

        if not os.path.exists(path):
            os.makedirs(path)
            print("Create a directoty {}".format(path))

    def set_export_file_name(self, fileName):
        name = self.params['dept_no'] if not fileName else fileName
        if self.params["syear"] and self.params["sem"]:
            self.fileName = "{}_{}_{}.json".format(name, year, semester)
        else:
            self.fileName = "{}.json".format(name)

    def export(self, fileName=None, path='./course_result'):
        self.set_expor_path(path)
        self.set_export_file_name(fileName)

        courses = self.get_courses()
        with open("{}/{}".format(self.path, self.fileName), 'w') as f:
            f.write(json.dumps(courses, ensure_ascii=False, indent=4))


class NoCourseAvailableError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


if __name__ == '__main__':
    import sys

    arg_num = len(sys.argv)

    if (arg_num is 2):
        _, dept_no = sys.argv
        parser = NckuCourseParser(dept_no)
    elif (arg_num is 4):
        _, dept_no, year, semester = sys.argv
        if (year[0] != 0):
            year = "0" + str(year)
        parser = NckuCourseParser(dept_no, year, semester)
    else:
        print("arg_num should be one or three.\n"
              "one: dept_no\n"
              "three: dept_no year semester")
        exit()

    try:
        parser.set_field(['系號',
                          '序號',
                          '課程名稱(連結課程地圖)',
                          '學分',
                          '教師姓名*:主負責老師',
                          '已選課人數',
                          '餘額',
                          '時間',
                          '教室'])
        parser.export()
    except NoCourseAvailableError as e:
        print(e)
    except Exception as e:
        print(e)
