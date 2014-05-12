import lib.NCKUcourseChecker as NCKUcourseChecker
import os

if __name__ == '__main__':
    while(True):
        parser = NCKUcourseChecker.NCKUcourseChecker()
        departmentNo = input("請輸入系所代號:")
        parser.setDepartmentNo(departmentNo)
        parser.setURL()
        parser.parseCourseData()
        parser.filterInfo()
        parser.sortedThroughtRemainder()
        result = parser.getFilteredTable()
        for i in range(len(result)):
            for j in range(len(result[i])):
                print(result[i][j], end="\t")
            print ()
