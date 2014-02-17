import NCKUcourseParser
import urllib.request
from operator import itemgetter
if __name__ == '__main__':
    departmentNo = input("請輸入系所代碼 : ")

    URL = "http://140.116.165.74/qry/qry001.php?dept_no=" + departmentNo
    web = urllib.request.urlopen(URL)
    webContent = web.read().decode("utf8")
    web.close()

    parser = NCKUcourseParser.courseParser()
    for line in webContent.splitlines():
        parser.feed(line)

    filterCondition = ["系號","序號","課程名稱(連結課程地圖)","學分","教師姓名*:主負責老師","餘額 ","時間","教室"]
    filteredIndex = []
    for i in range(len(parser.titles)):
        if parser.titles[i] in filterCondition:
            filteredIndex.append(i)

    filteredCourseInfo = []
    for i in range(len(parser.courses)):
        filteredCourseInfo.append([parser.courses[i][j] for j in filteredIndex])

    print (filterCondition)
    filteredCourseInfo = sorted(filteredCourseInfo, key=itemgetter(5))
    for i in range(len(filteredCourseInfo)):
        print (filteredCourseInfo[i][5])
