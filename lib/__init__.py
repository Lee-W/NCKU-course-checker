from .NCKUcourseFilter import NCKUcourseFilter
from .NCKUcourseParser import NCKUcourseParser

class NCKUcourseChecker:
    def __init__(self):
        self.parser = NCKUcourseParser()
        self.courseFilter = NCKUcourseFilter()

        self.title = self.courseFilter.filterCondition

        self.courseInfo = ""

    def setDepartmentNo(self, dNo):
        self.parser.setURL(dNo)

    def getFilteredCourseData(self):
        self.parser.parseWebForm()
        courseInfo = self.parser.getCourseForm()

        self.courseFilter.setCourseData(courseInfo)
        self.courseFilter.filterInfo()
        self.courseFilter.sortData()
        return self.courseFilter.getFilteredData()

    def reset(self):
        self.courseFilter.reset()


if __name__ == '__main__':
    checker = NCKUcourseChecker()
    checker.setDepartmentNo("H3")
    print (checker.getFilteredCourseData())
