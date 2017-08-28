#Perspective Table Class PTable

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem, QTableWidget, QMenu)
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

import TableUI
import TableAttributesWin
import Annotate
import numpy as np
import pandas as pd


class CreateTable(QTableWidget):
    ScatterDataSignal = pyqtSignal(list, np.ndarray)    #Signal emitted to send x,y data to create Scatter Plot
    BoxDataSignal = pyqtSignal(list, pd.DataFrame, int)  # Signal Emitted to send y data, statistics data, row index number to create Box Plot
    reNameSignal = pyqtSignal(str, str)  # signal to send the previous name of the table and the assigned new name
    AnnotationSignal = pyqtSignal(list)   #signal passes list of annotations



    def __init__(self, Data, row, col, colHeaders, StatsInfo):
        super(CreateTable, self).__init__()

        #row = length of row headers
        #col = length of col headers
        #colHeaders = string name for Alpha Parts
        #StatsInfo = statics data
        #data =  measurements not stats data

        self.AnnotationList = []  # stores a list of all annotations for this particular table

        print("Start initialization: Table Creation is underway")

        self.name = "temporary name"    #create variable to store table names

        self.StatsInfo = StatsInfo
        print(self.StatsInfo)

        self.setSelectionBehavior(self.SelectRows) #on click table highlights a row instead of a cell

        #assigning table properties of length, headers, data
        self.ColHeaders = colHeaders
        self.setRowCount(row)
        self.setColumnCount(col)
        self.data = Data
        self.setHorizontalHeaderLabels(colHeaders)


        print("Initiating for loop to assign data to QTableWidget")

        self.LenRowIndex = len(Data)
        self.LenColHeaders = len(colHeaders)

        for i in range(self.LenRowIndex):
            DataValues = self.data.iloc[i, :]   #loop through Row Index and grab all data in the row
            print("values are {}".format(DataValues))

            #converts these values from pandas table object to list format
            ValList = DataValues.values.tolist()

            #loops through DataValues list and assigns it to the appropriate cell in the QTable, to 3 significant digits
            for j in range(0, self.LenColHeaders):
                item = QTableWidgetItem(str(round(ValList[j], 6)))
                self.setItem(i, j, item)

    def contextMenuEvent(self, event):

        menu = QMenu(self)  #creates a menu that opens when table is right-clicked

        ###Options added to menu###
        boxAction = menu.addAction("Box Plot")
        scatterAction = menu.addAction("Scatter Plot")
        menu.addSeparator()

        AnnotateAction = menu.addAction("Annotate")
        menu.addSeparator()

        ReNameAction = menu.addAction("Rename")
        printNameAction = menu.addAction("Name?")
        printAction = menu.addAction("Print Row")

        menu.addSeparator()
        resetAction = menu.addAction("Reset Table")
        quitAction = menu.addAction("Close Table")
        menu.addSeparator()
        checkAttributesAction = menu.addAction("Properties")  ###checkAttributes open a settings-esque window


        action = menu.exec_(self.mapToGlobal(event.pos()))  #tracks the mouse and saves the position of an event(action)

        if action == quitAction:    #close table
            self.deleteLater()

        elif action == printAction: #outputs the selected row to the console
            self.selected = self.selectedItems()    #selected items refers to the selection behavior and will be a row of QTable items
            n = len(self.selected)
            print("n is {}".format(n))
            # to use Qtable Items must be converted from item -> string -> float
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                self.selected[i] = float(self.selected[i])
            print(self.selected)

        ###Attribute Naming related actions###
        elif action == resetAction: #if any changes (i.e removing value from Qtable) user can reset to its original data
            for i in range(self.LenRowIndex):
                # DataValues grabs a row of data from dataframe
                DataValues = self.data.iloc[i, :]
                print("values are {}".format(DataValues))

                # converts these values into list format
                ValList = DataValues.values.tolist()

                # loops through DataValues list and assigns it to the appropriate cell in the QTable, to 3 significant digits
                for j in range(0, self.LenColHeaders):
                    item = QTableWidgetItem(str(round(ValList[j], 6)))
                    self.setItem(i, j, item)

        elif action == ReNameAction:    #action lets you change the name of the table
            self.openPop = TableUI.TablePopup() #create an instance of the tableUI
            self.openPop.show()
            self.openPop.TableString.connect(self.RenameTable) #runs the rename method

        elif action == checkAttributesAction:
            print("Opening table properties")
            self.selected = self.selectedItems() #sets variable selected to be the row highlighted when clicked
            self.Row_Selection = self.row(self.selected[1])
            print(self.Row_Selection)

            try:
                #create object using module TableAttritbutesWin.py, pass arg table name, statistics, row index number
                self.AttributesWindow = TableAttributesWin.AttributesDialog(self.name, self.StatsInfo,self.Row_Selection)
                self.AttributesWindow.show()
            except Exception as TableAttErr:
                print("error occured when creating the Table Attritbute window.......ERROR: {}".format(TableAttErr))

        elif action == printNameAction:
            #returns name of table via console
            print(self.name)
        elif action == AnnotateAction:
            print("Annotation has been called")
            self.AnnotatedWin = Annotate.TextBoxAnnotation()
            self.AnnotatedWin.exec_()

            self.AnnotationList.append(self.AnnotatedWin.Annotation)
            print(self.AnnotationList)
            print("annotations have been appended to list")

            self.AnnotationSignal.emit(self.AnnotationList)

            print("signal has been emitted")


        ###GRAPHING COMMANDS###
        elif action == boxAction:
            print("Box Plot Called from context menu")

            try:
                self.selected = self.selectedItems()
                self.RowNum = self.currentRow() #reports what row of the QtableWidget we selected
                print(self.RowNum)

                n = len(self.selected)
                for i in range(n):
                    self.selected[i] = str(self.selected[i].text())
                for i in range(n):
                    if self.selected[i] != "":  #if the selected has empty string values they are replace with float nulls
                        self.selected[i] = float(self.selected[i])
                    else:
                        self.selected[i] = np.nan
                        pass
                print("right before plotter called")

                self.BoxDataSignal.emit(self.selected, self.StatsInfo, self.RowNum) #emit signal carrying all the data to be plotted
            except Exception as boxSignalErr:
                print("Right when box plot is called an error cccurs and crashes the program. ERROR: {}".format(boxSignalErr))

        elif action == scatterAction:
            print("Scatter Plot Called from context menu")
            self.selected = self.selectedItems()
            n = len(self.selected)
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                if self.selected[i] != "":
                    self.selected[i] = float(self.selected[i])
                else:
                    self.selected[i] = np.nan
                    pass
            print("right before plotter called")

            self.ScatterDataSignal.emit(self.selected, self.ColHeaders) #emit signal carrying all the data to be plotted

        else:
            print("A menu action was not clicked")

    def RenameTable(self, TableName):
        #Function responsible for renaming the table

        currentName = self.name     #store name when rename is clicked from context menu
        print("inside RenameTable")
        self.name = TableName   #the new name given by user
        print(self.name)

        self.reNameSignal.emit(currentName, self.name) #emit signal to finalize name change


    # def NameChange(self, string):
    #     print("name change initiate")
    #     self.name = string
    #     print("table name is {}".format(self.name))

    def rowbyIndex(self, row):

        #row = row index number of a table

        self.NullIndex = []
        self.MultiRowList =[]
        if row < self.rowCount():   #loops through rows of the table
            for j in range(self.columnCount()): #loops through columns
                if self.item(row,j).text() == "":   #checks to see if cell is empty (has a null value)
                    self.NullIndex.append(j)    #if cell is empty we save the index so we can delete that data pt later on
                else:
                    # if not empty we add the cell to data to be plotted
                    self.MultiRowList.append(float( self.item(row, j).text() ))

        return(self.MultiRowList, self.NullIndex)