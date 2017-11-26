import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'
executables = [cx_Freeze.Executable("test.py", base=None)]

cx_Freeze.setup(
    name="FDDS",
    options = {"build_exe": {"packages":{"numpy"}}},
    version = "0.01",
    description = "FDDS",
    executables = executables
)
# from cx_Freeze import setup, Executable
#
# setup(
#     name = "FDDS",
#     version = "1.0",
#     description = "FDDS",
#     executables = [Executable("index.py", base = "Win32GUI")])