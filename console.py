from lib import NCKUcourseChecker
import os

if __name__ == '__main__':
    while True:
        checker = NCKUcourseChecker()
        departmentNo = input("請輸入系所代號 (如要離開，請輸入-1) : ")
        if (departmentNo == "-1"):
            break
        checker.setDepartmentNo(departmentNo)
        result = checker.getFilteredCourseData()
        for i in range(len(result)):
            for j in range(len(result[i])):
                print(result[i][j], end="\t")
            print ()
