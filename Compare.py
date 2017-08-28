from PyQt5.QtCore import QRegularExpression, pyqtSignal
from PyQt5.QtGui import QIcon, QRegularExpressionValidator, QValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout,QPushButton, QSpacerItem, QSizePolicy

import Selector

class CompareDialog(QDialog):
    def __init__(self, names, parent=None):
        QDialog.__init__(self, parent)

        print("Initializing Compare Dialog")

        #main layout set to be Vbox
        self.setLayout(QVBoxLayout())
        self.setWindowTitle("Perspective - MultiGraph Window")

        self.names = names          #saves name of the table
        self.selectWidgetList = []  #List that will hold selector widget objects
        self.config = {}            #dictionary that will hold the plot type and row data

        ly = QHBoxLayout()
        ly.addWidget(QLabel("Input Format Table Name row, numbers, seperated, with, commas", self))

        addBtn = QPushButton("Add", self)
        addBtn.clicked.connect(self.addSelections)
        addBtn.setAutoDefault(False)
        ly.addWidget(addBtn)
        self.layout().addLayout(ly)

        #layout specifically for selector widget
        self.selectionsLayout = QVBoxLayout()
        self.layout().addLayout(self.selectionsLayout)

        hlayout = QHBoxLayout()
        hlayout.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        self.boxPlot = QPushButton("Box Plot", self)
        self.scatterPlot = QPushButton("Scatter Plot", self)

        #prevents box/scatter btns from being pressed until proper input is given
        self.boxPlot.setEnabled(False)
        self.scatterPlot.setEnabled(False)

        self.boxPlot.clicked.connect(self.onCliked)
        self.scatterPlot.clicked.connect(self.onCliked)
        hlayout.addWidget(self.boxPlot)
        hlayout.addWidget(self.scatterPlot)

        self.addSelections()

        self.layout().addLayout(hlayout)

    def onCliked(self):

        print("Plot Command has been issued")

        if self.sender() == self.boxPlot:   #checks to see which button in the compare window was pressed
            print(self.config)
            self.config['type'] = 'box'
        else:
            self.config['type'] = 'scatter'

        selected = []

        #w is a selector object
        for selector in self.selectWidgetList:
            selected.append(selector.getRows())    #grabs user row input
        self.config['values'] = selected    #assigns data from table as values

        self.accept()

    def addSelections(self):
        selector = Selector.SelectionWidget(self.names, self)   #creates a selector object

        #allows for box/scatter plot btns to be pressed
        selector.completed.connect(self.boxPlot.setEnabled)
        selector.completed.connect(self.scatterPlot.setEnabled)

        try:
            self.selectWidgetList.append(selector)     #everytime a new selector widget is created save it in a list
            self.selectionsLayout.addWidget(selector)  #add to our layout
        except Exception as selectorListErr:
            print("error occurred when trying to append selector widget to object list........ERROR:{}".format(selectorListErr))