from lib.NCKU_course_crawler import NckuCourseCrawler


def test_getURL():
    crawler = NckuCourseCrawler(dept_no="AN", year="0103", semester="1")
    assert "syear=0103" in crawler.get_URL()
    assert "sem=1" in crawler.get_URL()
    assert "dept_no=AN" in crawler.get_URL()
    assert "http://140.116.165.74/qry/qry002.php" in crawler.get_URL()
