import sys
from cx_Freeze import setup, Executable


import sqlite3
import os
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import builder



# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
icon = "icon.ico"


if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "interface",
        version = "2.0",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Projeto_main.py", base=base, icon=icon)])