from NCKU_course_checker.NCKU_course_checker import NckuCourseChecker

if __name__ == '__main__':
    while True:
        departmentNo = input("請輸入系所代號 (如要離開，請輸入-1) : ")
        if (departmentNo == "-1"):
            break
        checker = NckuCourseChecker(departmentNo)
        checker.get_courses(sort=True, ascending=False)
        checker.print_courses_table()
        # checker.setDepartmentNo(departmentNo)
        # result = checker.getFilteredCourseData()
        # for i in range(len(result)):
            # for j in range(len(result[i])):
                # print(result[i][j], end="\t")
            # print ()
