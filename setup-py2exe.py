import py2exe
from distutils.core import setup

main_python_file = "GUI.py"
application_title = "NCKU Course Checker"
application_description = "App to query NCKU courses"

includes = ["tkinter",
            'nckucourseparser.nckucoursecrawler',
            'nckucourseparser.nckucourseparser']
excludes = []
packages = []
include_files = []
build_exe_options = {"includes": includes,
                     "excludes": excludes,
                     "packages": packages,
                     "include_files": include_files}
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name=application_title,
      version="0.2",
      description=application_description,
      author="LeeW",
      author_email="cl87654321@gmail.com",
      url="https://github.com/Lee-W/NCKU-course-checker",
      windows=['GUI.py'],
      options={"py2exe": {
                  "includes": includes
              }
      }
)
