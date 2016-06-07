class NckuCourseChecker():
    def __init__(self, courses):
        self.courses = courses

    def sort_courses(self, sort=True,
                    sort_field="餘額", ascending=False, delete_zero=True):

        self.courses.dropna(inplace=True)
        if delete_zero:
            self.courses = self.courses[self.courses['餘額'] != 0]

        if sort:
            self.courses = self.courses.sort_values(by=sort_field, ascending=ascending)
        return self.courses

    def print_courses_table(self):
        for field in self.courses.columns.values:
            print(field, end="\t\t")
        print()

        for index, row in self.courses.iterrows():
            for col in row:
                print(col, end="\t\t")
            print()