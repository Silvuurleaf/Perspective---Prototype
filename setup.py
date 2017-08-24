import sys
import matplotlib
from distutils.core import setup
import cx_Freeze
from cx_Freeze import setup, Executable

build_exe_options = dict(packages = [], excludes = [])

Thanks = ["PRMoureu","eyllanesc", "ImportanceOfBeingErnest"]

Packages = ["numpy", "numpy.lib.format", "matplotlib", "os", "PyQt5", "PyQt5.QtCore", "PyQt5.QtGui"]
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
    executables = [Executable("Perspective.py")]
    )
