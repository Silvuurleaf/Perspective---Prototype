import sys
from distutils.core import setup
import cx_Freeze
from cx_Freeze import setup, Executable

build_exe_options = dict(packages = [], excludes = [])
BigThanks2 = ["PRMoureu","eyllanesc"]

Packages = ["numpy", "numpy.lib.format", "os", "PyQt5", "PyQt5.QtCore", "PyQt5.QtGui"]
Include = ["BulkGrab.py", "DataClassifier.py", "Formatter.py", "StatsCalc.py", "Save.py"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name='Markintosh - Data Acquisition Manager',
    author='mtaylor - Mark L.A. Taylor',
    author_email='taylor26@seattleu.edu - subject to change',
    options={"build_exe": {"packages": Packages, "include_files": Include}},
    description='Data compiler for formatting CSV files from GEO-Magic Laser Scanner. Sultan, WA',
    executables = [Executable("DataCompiler.py")]
)

