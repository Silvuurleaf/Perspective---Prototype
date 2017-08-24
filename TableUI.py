from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel,QMainWindow)

from PyQt5.QtCore import Qt, pyqtSignal

class TablePopup(QMainWindow):
    """
        The purpose of TablePopup class is for when the user creates a table. We want to be able to identify
        this table later on so we want the user to give it a sepcifc name.
        TablePopup prompts the user with a small dialog box and asks for a some name to be inputted.

        The name is then emitted and the CreateTable class handles the string assigning it as its new name

    """

    TableString = pyqtSignal(str)

    def __init__(self):
        super(TablePopup, self).__init__()

        self.setWindowTitle("Table Properties")

        self.initTablePop()

    def initTablePop(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # submits user input when enter button is clicked
        self.enterBTN = QPushButton("Enter")
        self.enterBTN.clicked.connect(self.submitName)
        self.enterBTN.setMaximumSize(50, 20)

        # Accepts user input and connects to submit name code if the user hits enter after
        self.editName = QLineEdit("Enter Table Name")
        self.editName.setMaximumSize(100, 20)
        self.editName.returnPressed.connect(self.enterBTN.click)

        ###LAYOUT###
        self.Main = QVBoxLayout(self.main_widget)

        self.hor1 = QHBoxLayout()
        self.hor1.addWidget(self.editName)
        self.hor1.addWidget(self.enterBTN)

        self.Main.addLayout(self.hor1)

    def submitName(self):
        # Once enter is hit or enter button is clicked then the signal is emitted containg the new name
        print("name has been changed")
        TableName = self.editName.text()
        print(TableName)
        self.TableString.emit(TableName)

        # after submission popupbox closes
        self.close()
