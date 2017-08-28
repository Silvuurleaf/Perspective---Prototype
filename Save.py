from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QFileDialog, QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
class FileSave(QDialog):
    def __init__(self, UnsavedData):
        super(FileSave, self).__init__()

        try:
            self.UnsavedData = UnsavedData
            self.SaveMenu = QtWidgets.QDialog()

            self.errorBox = QtWidgets.QErrorMessage()

            self.setLayout(QVBoxLayout())

            Hbox1 = QHBoxLayout()
            Hbox2 = QHBoxLayout()

            self.SaveEdit = QLineEdit("Save file as...")
            Hbox1.addWidget(self.SaveEdit)

            SaveBtn = QPushButton("Save", self)
            SaveBtn.clicked.connect(self.SaveLocale)
            Hbox2.addWidget(SaveBtn)

            CancelBtn = QPushButton("Cancel", self)
            CancelBtn.clicked.connect(self.Cancel)
            Hbox2.addWidget(CancelBtn)

            self.layout().addLayout(Hbox1)
            self.layout().addLayout(Hbox2)

            self.exec_() #when functions is called starts up QDialog window

        except Exception as QDlog:
            print("error occured when trying to utilize save QDialogwindow...... ERROR: {}".format(QDlog))

    def SaveLocale(self):
        try:
            print("inside SaveLocale")

            self.filename = self.SaveEdit.text()        #takes whatever text was input to QLineEdit before save btn was hit
            self.savepath = QFileDialog.getExistingDirectory() #opens a window ask where to save file, then saves filepath
            if self.savepath == "" or self.filename == "":
                #checks to see if the filepath or filename is empty and returns an error
                self.errorBox.showMessage("Invalid Input!")
            else:
                self.UnsavedData.to_csv(("{}/{}.csv").format(self.savepath, self.filename)) #saves file using filepath and filename defined by user
                print("File successfully transfered to........{}".format(self.savepath))
                self.close()
        except Exception as SaveErr:
            print("error found when trying to save file....ERROR: {}".format(SaveErr))

    def Cancel(self):
        self.close()