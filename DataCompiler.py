#!/usr/bin/env python
# -*- coding: utf-8 -*-

#above code is for encoding allows pandas to read in certain csv files.
# Makes the program more flexible

"""
    Program name - DataCompiler.py
    Written by - Mark Taylor (Taylor26@seattleu.edu or Markuslataylor@gmail.com
    Date and version No:  9/15/17

    Purpose: Sets up MainWindow and prompts user to dictate a filepattern for which the program will search for when
            compiling the files.

    Main Executable Tree: All other modules are branched off from this file.
    Inputs: Optional input allows the user to decide what type of FilePattern will be used to grab files
    Outputs: Will out main formatted file to the Save.py file, which will then be saved as a .csv file
"""

import os
import urllib
import json
#above are old modules used with tkinter

import sys
import pandas as pd

import BulkGrab
import DataClassifier
import Formatter
import StatsCalc
import Save

from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget,QMainWindow, QLineEdit)


class MainWindow(QMainWindow):  #Our class MainWindow inherits from the class in PyQt called QMainWindow
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Data Compiler")

        # Initializes the user interface window
        self.BootUpUI()

    def BootUpUI(self):
        print("widgets will be pulled up when executable is called")

        #create an object called main_widget that inherits from QWidget library
        self.main_widget = QWidget(self)

        #this widget is than set as the Windows main widget
        self.setCentralWidget(self.main_widget)

        #Creating Buttons/Widgets_______________________________________________________________________________________

        self.FileNameEdit = QLineEdit("Enter File Pattern...")

        self.ImportCompile = QPushButton("Import | Compile")
        self.ImportCompile.clicked.connect(self.FileImport)

        self.EndBtn = QPushButton("Close Window")
        self.EndBtn.clicked.connect(self.CloseFN)

        self.MainLayout = QHBoxLayout(self.main_widget)


        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.FileNameEdit)
        self.Vbox.addWidget(self.ImportCompile)
        self.Vbox.addWidget(self.EndBtn)

        self.MainLayout.addLayout(self.Vbox)

        self.TrendReportList = []

        self.show()
    def CloseFN(self):
        self.close()
    def FileImport(self):
        print("ImportingFile")
        try:
            self.FilePattern = self.FileNameEdit.text()
            print("FILE PATTERN COMING OUT")
            print(self.FilePattern)
            self.DataLocation = BulkGrab.DataList(self.FilePattern)         #Creates an object using DataList class in BulkGrab.py
        except Exception as FileLocationErr:
            print("error occured when grabbing file locations....ERROR: {}".format(FileLocationErr))
        print("after DataLocation")

        try:
            #check
            if self.DataLocation.NoneReturn == True:
                print("None type is true")
                pass
            else:
                self.filesLocations = self.DataLocation.filepaths    #Gathers a list of the file paths of each file that will be merged

                self.FileSearch()
        except Exception as NoneReturnErr:
            print("error occured when checking none-type value.......ERROR:{}".format(NoneReturnErr))

    def FileSearch(self):
        NumberOfFiles = len(self.filesLocations)

        self.PastTrendReport = pd.DataFrame()    #Variable to store trend reports as we iterate through multiple reports
        """
            For each trend report we create an Object PastTrendReport using the DataClassifier.py file and the class File_Attributes.
            
            The file is opened, read, and then converted to a pandas dataframe. From there the data is classified in the Files_attributes class
            The object is then stored in a list which will eventually contain all the trendreports grabbed.
            
            CHECK TERMINOLOGY FOR INFORMATION ON ENCODING
            encoding="ISO-8859-1" is so that the program can read incoming CSV. There was one csv file my program couldn't read and this fixed that problem.
            UTF-8 is a multibyte encoding that can represent any Unicode character
            ISO-8859-1 is a single-byte encoder can represent first 256 Unicode characters
        """

        for i in range(NumberOfFiles):
                self.PastTrendReport = DataClassifier.File_Attributes(pd.read_csv(open((self.filesLocations[i]), encoding="ISO-8859-1")))
                self.TrendReportList.append(self.PastTrendReport)

        self.CallFormat(self.TrendReportList)

    def CallFormat(self, TrendReports):
        self.FormattedObject = Formatter.Reformat(TrendReports)     #creates an object from the file Formatter.py and the class Reformat
                                                                    #Object should include actual values and nominal/tolerance measurements in the form of a Pandas Dataframe

        self.DataAndStats = StatsCalc.DataStatistics(self.FormattedObject)          #calls the file StatsCalc.py and the class DataStatistics
                                                                                    #calculates statistical information appends itself to the dataframe

        UnSavedData = self.DataAndStats.CompletedData        #Looks into the object DataAndStats and grabs the CompletedData (Actual Values, Nominal/Tol, and Stats calculations)

        self.CallSave(UnSavedData)

    def CallSave(self, Unsaved):
        Save.FileSave(Unsaved)

        try:
            #Once fil has been saved we clear out the data so if we use the program again it doesn't merge the old file as well
            self.DataAndStats = None
            self.PastTrendReport = None
            self.TrendReportList = []
        except Exception as ClearData:
            print("an error occured while trying to reset the data.........ERROR: {}".format(ClearData))


def main():
    # main loop is run so that the window remains until the user exits the program
    app = QApplication(sys.argv)

    # window is an instance of the class MainWindow
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__.endswith('__main__'):
    #== "__main__":
    main()