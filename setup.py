import sys

from cx_Freeze import setup, Executable

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

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name=application_title,
      version="0.2",
      description=application_description,
      author="LeeW",
      author_email="cl87654321@gmail.com",
      url="https://github.com/Lee-W/NCKU-course-checker",
      options={"build_exe":  build_exe_options},
      executables=[Executable(main_python_file, base=base)]
      )
