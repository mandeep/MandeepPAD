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
        self.status_bar = self.statusBar()

        self.file_name = ""

    def initMenuBar(self):
        menubar = self.menuBar()
        file = menubar.addMenu('File')
        edit = menubar.addMenu('Edit')
        preferences = menubar.addMenu('Preferences')
        help_menu = menubar.addMenu('Help')

        self.newAction = QAction('New', self)
        self.newAction.setStatusTip('Create a new document.')
        self.newAction.setShortcut('CTRL+N')
        self.newAction.triggered.connect(self.new_file)

        self.openAction = QAction('Open', self)
        self.openAction.setStatusTip('Open an existing document.')
        self.openAction.setShortcut('CTRL+O')
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QAction('Save', self)
        self.saveAction.setStatusTip('Save the current document.')
        self.saveAction.setShortcut('CTRL+S')
        self.saveAction.triggered.connect(self.save_file)

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)

    def new_file(self):
        new_window = TextEditor(self)
        new_window.show()

    def open_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if self.file_name:
            with open(self.file_name) as file:
                self.text.setText(file.read())

    def save_file(self):
        if not self.file_name:
            self.file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')

        with open(self.file_name, 'w') as file:
            file.write(self.text.toPlainText())


def main():
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(application.exec_())

main()
