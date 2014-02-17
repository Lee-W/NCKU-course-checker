import NCKUcourseParser
import urllib.request
from operator import itemgetter
from tabulate import tabulate


if __name__ == '__main__':

    departmentNo = input("請輸入系所代碼 : ")

    URL = "http://140.116.165.74/qry/qry001.php?dept_no=" + departmentNo
    web = urllib.request.urlopen(URL)
    webContent = web.read().decode("utf8")
    web.close()

    parser = NCKUcourseParser.courseParser()
    for line in webContent.splitlines():
        parser.feed(line)

    # filterCondition = ["系號", "序號", "課程名稱(連結課程地圖)", "學分", "教師姓名*:主負責老師", "餘額 ", "時間"]
    filterCondition = ["系號", "序號", "課程名稱(連結課程地圖)",  "餘額 ", "時間"]
    filteredIndex = []
    title = parser.getTitle()
    for i in range(len(title)):
        if title[i] in filterCondition:
            filteredIndex.append(i)

    filteredCourseInfo = []
    for i in range(len(parser.getContent())):
        if parser.getContent()[i][15] > '0':
            filteredCourseInfo.append([parser.getContent()[i][j] for j in filteredIndex])

    filteredCourseInfo = sorted(filteredCourseInfo, key=itemgetter(3), reverse=True)
    formatStr = "{0:2}\t{1:3}\t{2:25s}\t{3}\t{4}"
    for i in filteredCourseInfo:
        print (formatStr.format(*i))

    # print (tabulate(filteredCourseInfo, headers=filterCondition, tablefmt='pipe'))
