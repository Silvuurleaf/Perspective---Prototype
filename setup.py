#Python file that tells you what packages/modules that are to be packaged together in the program

import sys
import matplotlib
from distutils.core import setup
import cx_Freeze
from cx_Freeze import setup, Executable

# creates a dictionary that stores our packages(libraries used) and libraries we don't want to include in our project
build_exe_options = dict(packages = [], excludes = [])

#some people who helped me make the program (StackOverflow usernames)
Thanks = ["PRMoureu","eyllanesc", "ImportanceOfBeingErnest"]


Packages = ["numpy", "numpy.lib.format", "matplotlib", "os", "PyQt5", "PyQt5.QtCore", "PyQt5.QtGui"]    #libraries used
Include = ["TableAttributesWin.py", "Compare.py", "CreateFigure.py", "PTable.py", "TableUI.py", "Selector.py" ]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name="Perspective",
    author='mtaylor - Mark L.A. Taylor',
    author_email='taylor26@seattleu.edu',
    options={"build_exe":{"packages":Packages,"include_files":Include}},
    description = "Data analysis and visualisation software",
    executables = [Executable("Perspective.py")]    #main file where the setup.py starts compiling programs
    )
