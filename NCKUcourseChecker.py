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

    filterCondition = ["系號", "序號", "課程名稱", "學分", "教師姓名", "餘額 ", "時間"]
    filteredIndex = []
    title = parser.getTitle()
    for i in range(len(title)):
        if title[i][0] in filterCondition:
            filteredIndex.append(i)

    filteredCourseInfo = []
    for i in range(len(parser.getContent())):
        filteredCourseInfo.append([parser.getContent()[i][j] for j in filteredIndex])

    filteredCourseInfo = sorted(filteredCourseInfo, key=itemgetter(5))
    formatStr = "{0}\t{1}\t{2}\t\t{3}\t{4}\t{5}\t{6}"
    for i in range(len(filteredCourseInfo)):
        print (formatStr.format(*filteredCourseInfo[i]))
