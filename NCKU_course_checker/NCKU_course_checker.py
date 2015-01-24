from operator import itemgetter
from .NCKU_course_parser.NCKU_course_parser import NckuCourseParser


class NckuCourseChecker():
    def __init__(self, dept_no, year="", semester=""):
        self._field = ["系號",
                       "序號",
                       "課程名稱(連結課程地圖)",
                       "學分",
                       "教師姓名*:主負責老師",
                       "餘額",
                       "時間"]

        self.parse = NckuCourseParser(dept_no, year, semester)
        self.parse.set_field(self._field)
        self.courses = self.parse.get_courses()

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        self._field = field
        self.parse.set_field(self._field)

    def get_courses(self, sort=False,
                    sort_field="餘額", ascending=True, delete_zero=True):
        if sort:
            self.__sort_data(sort_field, ascending, delete_zero)
        return self.courses

    def __sort_data(self, sort_field='餘額', ascending=True, delete_zero=True):
        for course in self.courses:
            course["餘額"] = 0 if course["餘額"] == "額滿" else int(course["餘額"])

        self.courses = sorted(self.courses,
                              key=itemgetter(sort_field),
                              reverse=not ascending)

        if delete_zero:
            self.courses = list(filter(lambda x: x["餘額"] != 0, self.courses))

    def print_courses_table(self):
        for field in self._field:
            print(field, end="\t")
        print()

        for course in self.courses:
            for field in self._field:
                print(course[field], end="\t")
            print()


if __name__ == '__main__':
    checker = NckuCourseChecker("h3", "0103", "1")
    checker.sort_data()
    print(checker.get_courses())
