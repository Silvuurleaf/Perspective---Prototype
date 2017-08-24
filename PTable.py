#Perspective Table Class

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem, QTableWidget, QMenu)
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

import TableUI
import TableAttributesWin
import numpy as np


class CreateTable(QTableWidget):
    dataSignal = pyqtSignal(list, np.ndarray, str)  # Signal Emitted to send x,y data for plotting
    reNameSignal = pyqtSignal(str, str)  # signal to send the previous name of the table and the assigned new name

    def __init__(self, Data, row, col, colHeaders, StatsInfo):
        super(CreateTable, self).__init__()

        print("Start initialization: Table Creation is underway")

        self.name = "temporary name"    # initiate a name to give to the table before the user assigns it a name.
        self.StatsInfo = StatsInfo

        self.setSelectionBehavior(self.SelectRows) #on click table highlights a row instead of a cell

        #assigning table properties of length, headers, data
        self.ColHeaders = colHeaders
        self.setRowCount(row)
        self.setColumnCount(col)
        self.data = Data
        self.setHorizontalHeaderLabels(colHeaders)


        print("Initiating for loop to assign data to QTableWidget")

        self.n = len(Data)
        self.m = len(colHeaders)

        for i in range(self.n):
            #DataValues grabs a row of data from dataframe
            DataValues = self.data.iloc[i, :]
            print("values are {}".format(DataValues))

            #converts these values into list format
            ValList = DataValues.values.tolist()

            #loops through DataValues list and assigns it to the appropriate cell in the QTable, to 3 significant digits
            for j in range(0, self.m):
                item = QTableWidgetItem(str(round(ValList[j], 6)))
                self.setItem(i, j, item)

    def contextMenuEvent(self, event):

        menu = QMenu(self)  #creates a menu that opens when table is right-clicked

        ###Options added to menu###
        boxAction = menu.addAction("Box Plot")
        scatterAction = menu.addAction("Scatter Plot")
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
            self.selected = self.selectedItems()
            n = len(self.selected)
            print("n is {}".format(n))
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                self.selected[i] = float(self.selected[i])
            print(self.selected)


        ###Attribute Naming related actions###
        elif action == resetAction: #if any changes (i.e removing value from Qtable) user can reset to its original data
            for i in range(self.n):
                # DataValues grabs a row of data from dataframe
                DataValues = self.data.iloc[i, :]
                print("values are {}".format(DataValues))

                # converts these values into list format
                ValList = DataValues.values.tolist()

                # loops through DataValues list and assigns it to the appropriate cell in the QTable, to 3 significant digits
                for j in range(0, self.m):
                    item = QTableWidgetItem(str(round(ValList[j], 6)))
                    self.setItem(i, j, item)

        elif action == ReNameAction:    #action lets you change the name of the table
            self.openPop = TableUI.TablePopup() #create an instance of the tableUI
            self.openPop.show()
            self.openPop.TableString.connect(self.RenameTable) #runs the rename method
        elif action == checkAttributesAction:
            print("Opening table properties")
            self.selected = self.selectedItems() #sets variable selected to be the row highlighted when clicked

            #rowwww = self.currentRow(self.selected[1])
            #print(rowwww)
            self.Row_Selection = self.row(self.selected[1])
            print(self.Row_Selection)

            try:
                self.AttributesWindow = TableAttributesWin.AttributesDialog(self.name, self.StatsInfo,self.Row_Selection)
                self.AttributesWindow.show()
            except Exception as TableAttErr:
                print("error occured when creating the Table Attritbute window.......ERROR: {}".format(TableAttErr))

        elif action == printNameAction:
            print(self.name)

        ###GRAPHING COMMANDS###
        elif action == boxAction:
            print("action clicked was box plot")
            try:
                self.selected = self.selectedItems()
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

                print(type(self.selected), type(self.ColHeaders))

                self.PlotVal = "box"

                self.dataSignal.emit(self.selected,self.ColHeaders, self.PlotVal) #emit signal carrying all the data to be plotted
            except Exception as boxSignalErr:
                print("Right when box plot is called an error cccurs and crashes the program. ERROR: {}".format(boxSignalErr))

        elif action == scatterAction:
            print("action clicked was scatter plot")
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

            print(type(self.selected), type(self.ColHeaders))

            self.PlotVal = "scatter"
            self.dataSignal.emit(self.selected, self.ColHeaders, self.PlotVal)

        elif action == checkAttributesAction:
            print("getting table specifics")
        else:
            print("A menu action was not clicked")
    def RenameTable(self, TableName):

        currentName = self.name
        print("inside RenameTable")
        self.name = TableName
        print(self.name)

        self.reNameSignal.emit(currentName, self.name)


    def NameChange(self, string):
        print("name change initiate")
        self.name = string
        print("table name is {}".format(self.name))

    def rowbyIndex(self, row):

        self.NullIndex = []
        self.MultiRowList =[]
        if row < self.rowCount():
            for j in range(self.columnCount()):
                if self.item(row,j).text() == "":
                    self.NullIndex.append(j)
                else:
                    self.MultiRowList.append(float( self.item(row, j).text() ))

        return(self.MultiRowList, self.NullIndex)