from lib import NCKUcourseChecker
import os

if __name__ == '__main__':
    pass
    while(True):
        checker = NCKUcourseChecker()
        departmentNo = input("請輸入系所代號:")
        checker.setDepartmentNo(departmentNo)
        result = checker.getFilteredCourseData()
        for i in range(len(result)):
            for j in range(len(result[i])):
                print(result[i][j], end="\t")
            print ()
