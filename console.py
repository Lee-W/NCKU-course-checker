from veryprettytable import VeryPrettyTable

from nckucourseparser.nckucoursecrawler import NckuCourseCrawler
from nckucourseparser.nckucourseparser import NckuCourseParser, NoCourseAvailableError


def print_courses_table(courses):
    for field in courses.columns.values:
        print(field, end="\t\t")
    print()

    for index, row in courses.iterrows():
        for col in row:
            print(col, end="\t\t")
        print()


if __name__ == '__main__':
    while True:
        dept_no = input("請輸入系所代號 (如要離開，請輸入-1) : ")
        if (dept_no == "-1"):
            break
        try:
            crawler = NckuCourseCrawler(dept_no=dept_no)
            html = crawler.get_raw_HTML()

            parser = NckuCourseParser(html)
            parser.include_fields = ["系號", "序號", "餘額", "課程名稱(連結課程地圖)", "學分", "教師姓名*:主負責老師", "時間"]
            courses = parser.parse(sort=True)

            table = VeryPrettyTable()
            table.field_names = courses.columns.values
            for i in courses.iterrows():
                table.add_row(i[1])
            print(table)
        except NoCourseAvailableError as e:
            print(e)
