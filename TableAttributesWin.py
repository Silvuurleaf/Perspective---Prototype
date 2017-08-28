import pandas as pd
from PyQt5.QtCore import QRegularExpression, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QRegularExpressionValidator, QValidator
from PyQt5.QtWidgets import QLineEdit,QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame


class AttributesDialog(QDialog):
    def __init__(self, name, StatsInfo, row,  parent=None):
        QDialog.__init__(self, parent)
        print("Inside Attributes Dialog")

        self.setLayout(QVBoxLayout())

        self.setWindowTitle("Table Properties")
        self.setMinimumSize(600,250)
        self.setMaximumSize(600,250)

        print(StatsInfo)
        print("printing row output.......{}".format(row))
        StatsDictionary = StatsInfo.iloc[[row]].to_dict()
        print("stats dictionary below")
        print(StatsDictionary)

        print("about to create nominal")


        Nominal = QLabel("Nominal")
        Nominal.setMinimumSize(95,20)
        NominalValue = QLineEdit(str(StatsDictionary['Nominal'][row]))
        NominalValue.setMaximumSize(40,20)
        print(StatsDictionary['Nominal'][row])

        print("nominal has been created")

        Name = QLabel("Table Name: {}".format(name))

        #Tolerance Stats
        Tolerance = QLabel("Tolerance")
        Tolerance.setMinimumSize(95,20)
        ToleranceValue = QLineEdit(str(StatsDictionary['Tolerance'][row]))
        ToleranceValue.setMaximumSize(55,20)
        print(StatsDictionary['Tolerance'][row])

        #Median
        Median = QLabel("Tolerance")
        Median.setMinimumSize(95,20)
        MedianValue = QLineEdit(str(StatsDictionary['Median'][row]))
        MedianValue.setMaximumSize(55,20)
        print(StatsDictionary['Median'][row])

        Mean = QLabel("Mean")
        Mean.setMinimumSize(95,20)
        MeanValue = QLineEdit(str(StatsDictionary['Mean'][row]))
        MeanValue.setMaximumSize(55,20)
        print(StatsDictionary['Mean'][row])

        Min = QLabel("Minimum")
        Min.setMinimumSize(95,20)
        MinValue = QLineEdit(str(StatsDictionary['Min'][row]))
        MinValue.setMaximumSize(55,20)
        print(StatsDictionary['Min'][row])

        Max = QLabel("Max")
        Max.setMinimumSize(95,20)
        MaxValue = QLineEdit(str(StatsDictionary['Max'][row]))
        MaxValue.setMaximumSize(55,20)
        print(StatsDictionary['Max'][row])

        Range = QLabel("Range")
        Range.setMinimumSize(95,20)
        RangeValue = QLineEdit(str(StatsDictionary['Range'][row]))
        RangeValue.setMaximumSize(55,20)
        print(StatsDictionary['Range'][row])

        Deviation = QLabel("Deviation")
        Deviation.setMinimumSize(95,20)
        DeviationValue = QLineEdit(str(StatsDictionary['Deviation'][row]))
        DeviationValue.setMaximumSize(55,20)
        print(StatsDictionary['Deviation'][row])

        StandardDeviation = QLabel("Standard Deviation")
        StandardDeviation.setMinimumSize(95,20)
        StdDevValue = QLineEdit(str(StatsDictionary['Standard Deviation'][row]))
        StdDevValue.setMaximumSize(75,20)
        print(StatsDictionary['Standard Deviation'][row])

        Variance = QLabel("Variance")
        Variance.setMinimumSize(95,20)
        VarianceValue = QLineEdit(str(StatsDictionary['Variance'][row]))
        VarianceValue.setMaximumSize(75,20)
        print(StatsDictionary['Variance'][row])

        LowerBound = QLabel("LowerBound")
        LowerBound.setMinimumSize(95,20)
        LowerBoundValue = QLineEdit(str(StatsDictionary['Lower Bound'][row]))
        LowerBoundValue.setMaximumSize(55,20)
        print(StatsDictionary['Lower Bound'][row])

        UpperBound = QLabel("UpperBound")
        UpperBound.setMinimumSize(95,20)
        UpperBoundValue = QLineEdit(str(StatsDictionary['Upper Bound'][row]))
        UpperBoundValue.setMaximumSize(55,20)
        print(StatsDictionary['Upper Bound'][row])

        self.UpBoundValue = StatsDictionary['Upper Bound'][row]
        self.LowerBoundValue = StatsDictionary['Upper Bound'][row]

        #Creating main layouts
        QH_NameBox = QHBoxLayout()
        QH_StatsHolder = QHBoxLayout()
        QSeperator = QHBoxLayout()

        VboxLeft = QVBoxLayout()
        VboxRight = QVBoxLayout()

        self.layout().addLayout(QH_NameBox)
        self.layout().addLayout(QSeperator)
        self.layout().addLayout(QH_StatsHolder)

        QH_NameBox.addWidget(Name)

        Seperator = QFrame()
        Seperator.setFrameShape(QFrame.HLine)
        QSeperator.addWidget(Seperator)

        QH_StatsHolder.addLayout(VboxLeft)
        QH_StatsHolder.addLayout(VboxRight)

        #Adding Stats Data to page
        # <editor-fold desc="Left Side Statistics">
        QNominal = QHBoxLayout()
        QNominal.addWidget(Nominal)
        QNominal.addWidget(NominalValue)
        QNominal.addStretch()
        VboxLeft.addLayout(QNominal)

        QTolerance = QHBoxLayout()
        QTolerance.addWidget(Tolerance)
        QTolerance.addWidget(ToleranceValue)
        QTolerance.addStretch()
        VboxLeft.addLayout(QTolerance)

        QMean = QHBoxLayout()
        QMean.addWidget(Mean)
        QMean.addWidget(MeanValue)
        QMean.addStretch()
        VboxLeft.addLayout(QMean)

        QMedian = QHBoxLayout()
        QMedian.addWidget(Median)
        QMedian.addWidget(MedianValue)
        QMedian.addStretch()
        VboxLeft.addLayout(QMedian)

        QMax = QHBoxLayout()
        QMax.addWidget(Max)
        QMax.addWidget(MaxValue)
        QMax.addStretch()
        VboxLeft.addLayout(QMax)

        QMin = QHBoxLayout()
        QMin.addWidget(Min)
        QMin.addWidget(MinValue)
        QMin.addStretch()
        VboxLeft.addLayout(QMin)

        # </editor-fold>

        # <editor-fold desc="Right Side Statistics">
        QRange = QHBoxLayout()
        QRange.addWidget(Range)
        QRange.addWidget(RangeValue)
        QRange.addStretch()
        VboxRight.addLayout(QRange)

        QDeviation = QHBoxLayout()
        QDeviation.addWidget(Deviation)
        QDeviation.addWidget(DeviationValue)
        QDeviation.addStretch()
        VboxRight.addLayout(QDeviation)

        QVariance = QHBoxLayout()
        QVariance.addWidget(Variance)
        QVariance.addWidget(VarianceValue)
        QVariance.addStretch()
        VboxRight.addLayout(QVariance)

        QStandardDeviation = QHBoxLayout()
        QStandardDeviation.addWidget(StandardDeviation)
        QStandardDeviation.addWidget(StdDevValue)
        QStandardDeviation.addStretch()
        VboxRight.addLayout(QStandardDeviation)

        QUpper = QHBoxLayout()
        QUpper.addWidget(UpperBound)
        QUpper.addWidget(UpperBoundValue)
        QUpper.addStretch()
        VboxRight.addLayout(QUpper)

        QLower = QHBoxLayout()
        QLower.addWidget(LowerBound)
        QLower.addWidget(LowerBoundValue)
        QLower.addStretch()
        VboxRight.addLayout(QLower)

        # </editor-fold>














