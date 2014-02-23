import sys
from cx_Freeze import setup, Executable

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"    # Tells the build script to hide the console.

setup(name = "NCKU course checker",
      version = "0.1",
      description = "to check whether particular deparment has any course that is not full (for NCKU only)",
      executables = [Executable("GUI.py")],
      options = {
        "GUI.py" : {
            "include-modules" : "html",
            "base-name" : base
        }
      }
      )
