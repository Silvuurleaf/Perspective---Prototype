#!/usr/bin/env python
# -*- coding: utf-8 -*-


# imports/libraries
# <editor-fold desc="Imports and Libraries">
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QSlider, QApplication, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel, QCheckBox, QRadioButton,QMainWindow,
                             QFileDialog, QMenu, QMessageBox, QAction, QToolBar, QDialog, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib import pyplot as plt
plt.style.use(['ggplot'])
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import csv
import pandas as pd

import linecache

#Custom Modules
import CreateFigure
import Compare #edwins version modified
import TableUI
import PTable



# </editor-fold>

class MainWindow(QMainWindow):
    """"
            Purpose: Mainwindow screen stores majority of application widgets.
            Responsible for displaying datatable and user interaction of upload, and datamanipulation

            Main function that uses sub function to branch off and connect to the other classes within this program

            Works as a sort of call center emitting signals that are transferred to appropriate classes when specific criteria are met
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Perspective")

        # Initializes the user interface window
        self.initializeUI()
        self.setMinimumSize(550,160)
        #calls the class TablePopWin to create the window to ask the user to name the table
        self.TablePopWin = TableUI.TablePopup()

    def initializeUI(self):

        # initiate list for table objects and dictionary to pair names with objects
        self.TableDB = []
        self.TableNameDB = []
        self.TableDictionary = {}


        ###set the main widget responsible for making widgets appear on scren
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)


        # CREATION OF WIDGETS GENERAL BUTTONS____________________________________________________________________________
        # <editor-fold desc="Widgets Creation CheckPoint">

        #Import Button related widgets
        self.FileNmLabel = QLabel('FileName')
        self.FileNameEdit = QLineEdit('"Filename"')
        self.FileNameEdit.setMaximumSize(380, 20)

        self.BrowseBtn = QPushButton('Browse')
        self.BrowseBtn.setMaximumSize(80, 20)
        self.BrowseBtn.clicked.connect(self.ImportFile)

        self.comparison = QPushButton('Compare')
        self.comparison.setMaximumSize(80, 20)
        self.comparison.clicked.connect(self.OpenCompare)


        # </editor-fold>__________________________________________________________________________END OF WIDGET CREATION


        # Widget Layout_________________________________________________________________________________________________
        # <editor-fold desc="Layout">

        self.hMAIN = QHBoxLayout(self.main_widget)

        ###Labels###
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.FileNmLabel)
        self.hbox2.addStretch()


        ###Widgets###
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.FileNameEdit)
        self.hbox3.addStretch()
        self.hbox3.addWidget(self.BrowseBtn)

        ###OverLay###
        self.hbox5 = QHBoxLayout()
        self.hbox5.addStretch()
        self.hbox5.addWidget(self.comparison)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox5)

        self.vboxRIGHT = QVBoxLayout()
        self.vboxData = QVBoxLayout()

        self.hMAIN.addLayout(self.vbox)
        self.vbox.addLayout(self.vboxData)

        # </editor-fold>


        self.show()

    def ImportFile(self):
        ###Actual importation and manipulation of Data CSV Files

        ### on click opens a dialog window asks user to pick a file from the directory and then stores the file's path.
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "(*.csv)")
        if fileName:
            print(fileName)
            self.FileNameEdit.setText(fileName)     #set text of LineEdit to be filename
            Data = pd.read_csv(open(fileName, encoding="ISO-8859-1"))   #reads csv and converts to a pandas DF
            # print(Data)

            ### removes all the statistics information from the file and reports just the raw data

            # <editor-fold desc="Data Reformatting Proccess">

            ###Saving the statistics data to be placed into a properties tab

            self.BaseStats = Data
            self.TableStats = pd.DataFrame()
            self.TableStats['Nominal'] = self.BaseStats['Nominal Value']
            self.TableStats['Median'] = self.BaseStats['median']
            self.TableStats['Tolerance'] = self.BaseStats['Tolerance']
            self.TableStats['Mean'] = self.BaseStats['mean']
            self.TableStats['Min'] = self.BaseStats['min']
            self.TableStats['Max'] = self.BaseStats['max']
            self.TableStats['Range'] = self.BaseStats['range']
            self.TableStats['Deviation'] = self.BaseStats['Deviation']
            self.TableStats['Variance'] = self.BaseStats['variance']
            self.TableStats['Standard Deviation'] = self.BaseStats['Standard Deviation']
            self.TableStats['Lower Bound'] = self.BaseStats['LowerBound']
            self.TableStats['Upper Bound'] = self.BaseStats['UpperBound']


            #self.BaseStats = Data.drop('Nominal Value', axis=1)
            self.BaseStats.drop('Nominal Value', axis=1, inplace=True)
            self.BaseStats.drop('median', axis=1, inplace=True)
            self.BaseStats.drop('Tolerance', axis=1, inplace=True)
            self.BaseStats.drop('mean', axis=1, inplace=True)
            self.BaseStats.drop('min', axis=1, inplace=True)
            self.BaseStats.drop('max', axis=1, inplace=True)
            self.BaseStats.drop('range', axis=1, inplace=True)
            self.BaseStats.drop('Deviation', axis=1, inplace=True)
            self.BaseStats.drop('variance', axis=1, inplace=True)
            self.BaseStats.drop('Standard Deviation', axis=1, inplace=True)
            self.BaseStats.drop('LowerBound', axis=1, inplace=True)
            self.BaseStats.drop('UpperBound', axis=1, inplace=True)
            self.BaseStats.drop('Unnamed: 0', axis=1, inplace=True)

            # print("Data has been dropped")
            # </editor-fold>

            #Grabs the index as the row headers, and grabs the column index to be the new column headers
            rowHeaders = self.BaseStats.index
            colHeaders = self.BaseStats.columns.values

            col = len(colHeaders)
            row = len(rowHeaders)

            print("SETTING UP THE ROW VALUE............................{}".format(row))
            print("Table is about to be created")

            # Create an instance of the table passing the data, number of rows and cols
            self.Table = PTable.CreateTable(self.BaseStats, row, col, colHeaders, self.TableStats)

            print("Table creation was successful")


            ### Table popup window is shown and ask for user to give newly defined table a name
            self.TablePopWin.show()


            # First popup window when table is created signal is sent
            self.TablePopWin.TableString.connect(self.NameAssignment)


            # connecting signal created after user renames a table from the context menu
            self.Table.reNameSignal.connect(self.ReNameAdjustments)

            # connects the emitted data signal to plot initiator
            self.Table.dataSignal.connect(self.SinglePlot)

            #embed the table widget
            self.vboxData.addWidget(self.Table)

    def NameAssignment(self, TableName):
        print("Name assignment method has been executed")
        #current name of the table is stored to be able to reference the dictionary
        #and the new name is assigned to the table's attributes
        oldName = self.Table.name
        self.Table.name = TableName

        print("adjusting table name database")


        #loops through dictionary untill we find the old key (old name of table) and then we replace it
        #this way the new table name is associated with the appropriate object
        for i in range(len(self.TableNameDB)):
            if self.TableNameDB[i] == oldName:
                self.TableNameDB[i] = TableName

        #DEBUGG checks
        #print(self.TableNameDB)
        #print(self.Table.name)

        print("Before TableDictionary undergoes reformatting")
        # print("List of table objects........... {}".format(self.TableDB))
        # print("List of table names..............{}".format(self.TableNameDB))
        # print("Dictionary.......................{}".format(self.TableDictionary))

        self.DataBaseHandler()

        # print("List of table objects........... {}".format(self.TableDB))
        # print("List of table names..............{}".format(self.TableNameDB))
        # print("Dictionary.......................{}".format(self.TableDictionary))

    def ReNameAdjustments(self, oldName, newName):
        print("rename has been called from the context menu on the QtableWidget")

        print("table name database before for loop")
        # print(self.TableNameDB)
        for i in range(len(self.TableNameDB)):
            if self.TableNameDB[i] == oldName:
                self.TableNameDB[i] = newName
        #print(self.TableNameDB)

        print("Before TableDatabase is altered")
        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

        self.DataBaseHandler()

        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

    def DataBaseHandler(self):
        print("Collecting table names and Qtable objects")

        self.TableDB.append(self.Table)            #Append Qtable Objects to list
        self.TableNameDB.append(self.Table.name)  # list stores all names of table objects
        self.TableDictionary = dict(zip(self.TableNameDB, self.TableDB)) #Combine the two above lists to make a dictionary

        print("Database has been adjusted")
    def OpenCompare(self):
        print("Booting up the CompareWindow")

        #creates an object comparWin to create an instace of Comparison Window UI and takes our Dictionary as an argument
        self.compareWin = Compare.CompareDialog(self.TableDictionary.keys())

        try:
            if self.compareWin.exec_() == QDialog.Accepted: #checks to see if proper input was given and calls Plot if it was
                self.PlotCatalyst(self.compareWin.config)
        except Exception as OpeningCompare:
            print("Error on opening compare window ERROR: {}".format(OpeningCompare))

    def PlotCatalyst(self, config):
        print("Inside Plot Catalyst")

        #grabs the values from the selector widget
        values = config['values']
        type_plot = config['type']

        print(config['values'])
        print(type_plot)

        #Create an instance of plot figure to plot data onto
        self.Multifigure = CreateFigure.FigureAssembly()

        for name, rows in values:   #loops through name and rows in values from selector widget
            print("about to iterate through values")

            table = self.TableDictionary[name]     #grabs object by refrencing Dictionary key
            tbHeaders = table.ColHeaders

            #loops through row list from selector Widget, checking given row for dataTable

            try:
                for row in rows:
                    # print("about to iterate through row values")
                    # print("printing row count {}".format(table.rowCount()))
                    # print("data type of row value: {}".format(type(row)))

                    if row < table.rowCount():  #loops through all the rows
                        print("2nd for loop embeded")
                        data, NullIndex = table.rowbyIndex(row) #outputs the data in the table and the index location
                        print("Printing data now")
                        print(data)
                        print(type_plot, name, row, data, tbHeaders)

                        #send multiplot signal to plot multiple reports on the same figure
                        self.initiateMultiPlot(type_plot, name, row, data, tbHeaders, NullIndex)
            except Exception as RowSelectorErr:
                print("error found when looping through selector widget values.......ERROR: {}".format(RowSelectorErr))

            self.ConfirmPlot(type_plot)


    def SinglePlot(self, x, y, PlotVal):

        print("Preparing singular plot construction")
        print(x)
        print(y)
        f = CreateFigure.FigureAssembly()   #create basic figure object for plotting
        f.plotData(x, y, PlotVal, True)     #from object we call method .plotData and pass our x,y data and plot the graph

    def initiateMultiPlot(self,type_plot, name, row, data, columnHeaders, NullIndex):

        #call the object Multifigure, instanstiated early in PlotCatalyst(), and call its method .MultiPlot
        #passes required arguments to plot several sets of data on the same figure
        self.Multifigure.MultiPlot(data,columnHeaders,type_plot,name, row, NullIndex, False)

    def ConfirmPlot(self, PlotV):
        print("Confirming finishes on plot collection")

        #Once all plots have been plotted on the figure we can show the user the figure
        #else if we showed it too early we wouldn't be able to include all the plots
        if PlotV == 'box':
            #not passing the table name so it can't grab the data from the table
            self.Multifigure.BoxPltter()
        else:
            self.Multifigure.ShowScatter()

def main():
    # main loop
    app = QApplication(sys.argv)
    # instance
    window = MainWindow()
    window.show()
    # appWindow = MainWindow()
    sys.exit(app.exec_())

if __name__.endswith('__main__'):
    #== "__main__":
    main()

