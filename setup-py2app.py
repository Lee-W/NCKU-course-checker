from setuptools import setup

main_python_file = "GUI.py"
application_title = "NCKU Course Checker"
application_description = "App to query NCKU courses"

includes = ['nckucourseparser.nckucoursecrawler',
            'nckucourseparser.nckucourseparser']
excludes = []
packages = []
include_files = []
build_exe_options = {"includes": includes,
                     "excludes": excludes,
                     "packages": packages,
                     "include_files": include_files}

setup(app=["GUI.py"],
      setup_requires=["py2app"],
      name=application_title,
      version="0.2",
      description=application_description,
      author="LeeW",
      author_email="cl87654321@gmail.com",
      url="https://github.com/Lee-W/NCKU-course-checker",
      options={"build_exe":  build_exe_options},
      )
