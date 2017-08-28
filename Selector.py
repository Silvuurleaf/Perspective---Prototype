from PyQt5.QtCore import QRegularExpression, pyqtSignal
from PyQt5.QtGui import QIcon, QRegularExpressionValidator, QValidator
from PyQt5.QtWidgets import QLineEdit,QHBoxLayout, QComboBox, QToolButton,QWidget

class SelectionWidget(QWidget):
    completed = pyqtSignal(bool)

    def __init__(self, items, parent=None):
        QWidget.__init__(self, parent)
        #Main Layout is a horizontal box
        self.setLayout(QHBoxLayout())

        #Create the drop down menu and fill it with the table names
        self.combobox = QComboBox(self)
        self.combobox.addItems(items)
        self.layout().addWidget(self.combobox)

        self.le = QLineEdit(self)
        self.le.setValidator(QRegularExpressionValidator(QRegularExpression("^([0-9])+(,[0-9]+)*$"), self))
        self.le.textChanged.connect(self.check_state)
        self.layout().addWidget(self.le)

        btnDelete = QToolButton(self)
        btnDelete.setIcon(QIcon.fromTheme("edit-delete"))
        self.layout().addWidget(btnDelete)
        btnDelete.clicked.connect(self.deleteLater)

    def getRows(self):
        try:
            return self.combobox.currentText(), [int(el) for el in self.le.text().split(",")]
        except Exception as p:
            print("error P: {}".format(p))

    def check_state(self, text):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(text, 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b'  # green
            self.completed.emit(True)
        elif state == QValidator.Intermediate:
            color = '#fff79a'  # yellow
            self.completed.emit(False)
        else:
            color = '#f6989d'  # red
            self.completed.emit(True)
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)