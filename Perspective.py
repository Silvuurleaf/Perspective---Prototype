#!/usr/bin/env python
# -*- coding: utf-8 -*-

# imports/libraries
# <editor-fold desc="Imports and Libraries">
#from PyQt5 import QtCore, QtGui, QtWidgets         Notsure if we even need these lines???
# from PyQt5.QtCore import Qt, pyqtSignal
import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel,QMainWindow,
                             QFileDialog, QDialog)
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib import pyplot as plt
plt.style.use(['ggplot'])

#Makes the plot figure layout Tight to ensure everything fits on the screen
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import pandas as pd

#Custom Modules imported from the same project folder
import CreateFigure
import Compare
import TableUI
import PTable
import DragHandler
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

        #self.AnnotationList = []    #stores a list of all annotations for this particular table
        self.Annotations = None

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

        self.show() #Shows

    def ImportFile(self):
        ###Actual importation and manipulation of Data CSV Files

        ### When import button is clicked opens a dialog window prompting user to pick a file from a directory and then stores the file's path.
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "(*.csv)")
        if fileName:
            print(fileName)
            self.FileNameEdit.setText(fileName)     #set text of LineEdit to be filename
            Data = pd.read_csv(open(fileName, encoding="ISO-8859-1"))   #reads csv and converts to a pandas DF
            # encoding is to be able to read different versions of CSV


            ### seperates raw Measurements from statistics data
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


            rowHeaders = self.BaseStats.index               #Grabs the index as the row headers
            colHeaders = self.BaseStats.columns.values      #Grabs the column index to be the new column headers

            NumOFcol = len(colHeaders)
            NumOFrow = len(rowHeaders)


            print("Table is about to be created")

            # Create an instance of the table passing the data, number of rows, cols, and statistics data
            self.Table = PTable.CreateTable(self.BaseStats, NumOFrow, NumOFcol, colHeaders, self.TableStats)

            print("Table creation was successful")

            ### Table popup window is shown and ask for user to give newly defined table a

            self.TablePopWin.show()

            # Once the table has been created a signal is emitted to open the Table Name Dialog Window
            self.TablePopWin.TableString.connect(self.NameAssignment)

            # When the user clicks rename feature, in the context menu, a signal is connected to rename the table
            self.Table.reNameSignal.connect(self.ReNameAdjustments)

            # Connects the scatter plot signal from context menu
            self.Table.ScatterDataSignal.connect(self.ScatterSinglePlot)

            # Connects the box plot signal from context menu
            self.Table.BoxDataSignal.connect(self.BoxSinglePlot)

            #connect annotations to the plot field
            self.Table.AnnotationSignal.connect(self.AddAnnotations)

            #Embeds the tablewidget into our mainwindow screen
            self.vboxData.addWidget(self.Table)
    def AddAnnotations(self, AnnotationList):
        # try:
        #     print("adding annotations to plot")
        #     print(AnnotationList)
        #     self.figure = CreateFigure.FigureAssembly()
        #     for i in AnnotationList:
        #         self.figure.plt.text(0,0,i, picker = True)
        #         dragh = DragHandler.DragHandler()
        # except Exception as AnnotationPltErr:
        #     print("error occured when trying to plot Annotations.....ERROR: {}".format(AnnotationPltErr))

        self.Annotations = AnnotationList

    def NameAssignment(self, TableName):
        print("Name assignment method has been executed")

        oldName = self.Table.name           #current name of the table is stored to be able to reference the dictionary
        self.Table.name = TableName         #and the new name is assigned to the table's attributes

        print("adjusting table name database")


        #loops through dictionary until we find the old key (old name of table) and then we replace it
        #this way the new table's name is associated with the appropriate instance of the table object
        for i in range(len(self.TableNameDB)):
            if self.TableNameDB[i] == oldName:
                self.TableNameDB[i] = TableName

        print("Before TableDictionary undergoes reformatting")
        # print("List of table objects........... {}".format(self.TableDB))
        # print("List of table names..............{}".format(self.TableNameDB))
        # print("Dictionary.......................{}".format(self.TableDictionary))

        self.DataBaseHandler()  #updates the dictionary in case anything was changed

        # print("List of table objects........... {}".format(self.TableDB))
        # print("List of table names..............{}".format(self.TableNameDB))
        # print("Dictionary.......................{}".format(self.TableDictionary))

    def ReNameAdjustments(self, oldName, newName):
        print("rename has been called from the context menu on the QtableWidget")

        #Works the same as name assignment. Replaces the keys for the table dictionary.

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
        self.TableNameDB.append(self.Table.name)   #list stores all names of table objects
        self.TableDictionary = dict(zip(self.TableNameDB, self.TableDB)) #Combine the two above lists to make our table dictionary

        print("Database has been adjusted")
    def OpenCompare(self):
        print("Booting up the CompareWindow")

        #creates an object comparWin to create an instace of Comparison Window UI and takes our Dictionary as an argument
        self.compareWin = Compare.CompareDialog(self.TableDictionary.keys())

        try:
            if self.compareWin.exec_() == QDialog.Accepted: #checks to see if proper input was given and calls Plot if it was
                self.PlotCatalyst(self.compareWin.config)
        except Exception as OpeningCompare:
            print("error occured when trying to open compare window ERROR: {}".format(OpeningCompare))

    def PlotCatalyst(self, config):
        print("Inside Plot Catalyst")

        #grabs the values from the selector widget
        values = config['values']
        type_plot = config['type']

        print(config['values'])
        print(type_plot)

        #values = list of RowLists
        #Rows = List of row indices from a table
        #Row = singular row index of  a table

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

    def BoxSinglePlot(self,y, StatsDataFrame, RowIndex):
        print("Preparing singular plot construction")
        try:
            self.figure = CreateFigure.FigureAssembly()              #create basic figure object that will hold our data
            print("HERE IS ANNOTATIONS.........................{}".format(self.Annotations))

            if self.Annotations != None:
                print("self.Anntations was not empty")
                self.figure.plotAnnotations(self.Annotations)

            self.figure.plotDataBox(y, StatsDataFrame, RowIndex)     #from object we call method .plotData and pass our x,y data and plot the graph


        except Exception as CreateBoxSingleFigureErr:
            print("About to create singualr boxplot but found an error........ERROR: {}".format(CreateBoxSingleFigureErr))

    def ScatterSinglePlot(self, x, y):

        print("Preparing singular plot construction")

        self.figure = CreateFigure.FigureAssembly()   #create basic figure object for plotting
        self.figure.ScatterPlotData(x, y)                    #from object we call method .plotData and pass our x,y data and plot the graph

    def initiateMultiPlot(self,type_plot, name, row, data, columnHeaders, NullIndex):

        #call the object Multifigure, instanstiated early in PlotCatalyst(), and call its method .MultiPlot
        #passes required arguments to plot several sets of data on the same figure
        self.Multifigure.MultiPlot(data,columnHeaders,type_plot,name, row, NullIndex)

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

