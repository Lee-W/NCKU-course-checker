import requests


class NckuCourseCrawler():
    def __init__(self, dept_no, year='', semester=''):
        self.courseQueryURL = "http://140.116.165.74/qry/qry002.php"
        self.params = {'syear': year, 'sem': semester, 'dept_no': dept_no}

    def set_year(self, year):
        self.params['syear'] = year

    def set_semester(self, semester):
        self.params['sem'] = semester

    def set_department(self, dept_no):
        self.params['dept_no'] = dept_no

    def get_raw_HTML(self):
        req = requests.get(self.courseQueryURL, params=self.params)
        req.encoding = 'utf-8'
        webContent = req.text
        return webContent

    def get_URL(self):
        req = requests.get(self.courseQueryURL, params=self.params)
        return (req.url)


if __name__ == '__main__':
    crawler = NckuCourseCrawler(year="0103", semester=1, dept_no="AN")
    raw_HTML = crawler.get_raw_HTML()
    print(raw_HTML)
