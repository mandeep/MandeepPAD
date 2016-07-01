import sys
from PyQt5.QtWidgets import *


class TextEditor(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('MandeepPAD')
        self.move(400, 200)

        self.initMenuBar()
        self.statusbar = self.statusBar()

        self.filename = ""

    def initMenuBar(self):
        menubar = self.menuBar()
        file = menubar.addMenu('File')
        edit = menubar.addMenu('Edit')
        preferences = menubar.addMenu('Preferences')
        help_menu = menubar.addMenu('Help')

        self.newAction = QAction('New', self)
        self.newAction.setStatusTip('Create a new document.')
        self.newAction.setShortcut('CTRL+N')
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction('Open', self)
        self.openAction.setStatusTip('Open an existing document.')
        self.openAction.setShortcut('CTRL+O')
        self.openAction.triggered.connect(self.open)

        file.addAction(self.newAction)
        file.addAction(self.openAction)

    def new(self):
        new_window = TextEditor(self)
        new_window.show()

    def open(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', '.', '(*.txt)')
        if self.filename:
            with open(self.filename, 'rt') as file:
                self.text.setText(file.read())


def main():
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(application.exec_())

main()
