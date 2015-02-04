application_title = "NCKU_course_checker"
main_python_file = "GUI.py"

import sys

from cx_Freeze import setup, Executable

build_exe_options = {"includes": ["tkinter", "NCKU_course_checker.NCKU_course_checker"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit","re"]

setup(
        name = application_title,
        version = "0.1",
        description = "Sample cx_Freeze Tkinter script",
        options = {"build_exe" : {"includes" : includes }},
        executables = [Executable(main_python_file, base = base)])

