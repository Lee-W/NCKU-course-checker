from NCKU_course_checker.NCKU_course_checker import NckuCourseChecker

def print_courses_table(checker):
    for field in checker.field:
        print(field, end="\t\t")
    print()

    courses = checker.get_courses(sort=True)
    for course in courses:
        for field in checker.field:
            print(course[field], end="\t\t")
        print()

if __name__ == '__main__':
    while True:
        departmentNo = input("請輸入系所代號 (如要離開，請輸入-1) : ")
        if (departmentNo == "-1"):
            break
        checker = NckuCourseChecker(departmentNo)
        print_courses_table(checker)
