
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel, QHBoxLayout,QPushButton


class TextBoxAnnotation(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        print("creating textbox")

        self.setLayout(QVBoxLayout())

        self.UserTextBox = QTextEdit("Enter Annotation Here")

        self.SubmitBtn = QPushButton("Submit")
        self.SubmitBtn.clicked.connect(self.AnnotateCreate)

        self.CloseBtn = QPushButton("Close")
        self.CloseBtn.clicked.connect(self.CloseCall)

        self.layout().addWidget(self.UserTextBox)
        self.layout().addWidget(self.SubmitBtn)
        self.layout().addWidget(self.CloseBtn)

    def AnnotateCreate(self):
        print("Take text from QTextEdit")

        try:
            if self.UserTextBox.toPlainText() != "Enter Annotation Here":
                self.Annotation = self.UserTextBox.toPlainText()
                print(self.Annotation)
            else:
                pass
        except Exception as TextEditErr:
            print("error creating annotation.......ERROR: {}".format(TextEditErr))
    def CloseCall(self):
        self.close()

