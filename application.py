import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog


class TextEditor(QMainWindow):
    """
    TextEditor class houses all of the methods needed to create the
    text editor application. The actual text editor window is initiated
    in the main() function which is called via entrypoint.
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.init_UI()

    def init_UI(self):
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('MandeepPAD')

        self.menu_bar()
        self.file_menu()

        self.file_name = None

        self.status_bar = self.statusBar()

    def menu_bar(self):
        menubar = self.menuBar()
        self.file = menubar.addMenu('File')
        self.edit = menubar.addMenu('Edit')
        self.preferences = menubar.addMenu('Preferences')
        self.help_menu = menubar.addMenu('Help')

    def file_menu(self):
        self.newAction = QAction('New File', self)
        self.newAction.setStatusTip('Create a new document.')
        self.newAction.setShortcut('CTRL+N')
        self.newAction.triggered.connect(self.new_file)

        self.openAction = QAction('Open File', self)
        self.openAction.setStatusTip('Open an existing document.')
        self.openAction.setShortcut('CTRL+O')
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QAction('Save File', self)
        self.saveAction.setStatusTip('Save the current document.')
        self.saveAction.setShortcut('CTRL+S')
        self.saveAction.triggered.connect(self.save_file)

        self.exitAction = QAction('Quit', self)
        self.exitAction.setStatusTip('Quit application.')
        self.exitAction.setShortcut('CTRL+Q')
        self.exitAction.triggered.connect(self.quit_application)

        self.file.addAction(self.newAction)
        self.file.addAction(self.openAction)
        self.file.addAction(self.saveAction)
        self.file.addAction(self.exitAction)

    def new_file(self):
        new_window = TextEditor(self)
        new_window.show()

    def open_file(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File')

        if self.file_name:
            with open(self.file_name) as file:
                self.text.setText(file.read())
            self.update_title()

    def save_file(self):
        if not self.file_name:
            self.file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')

        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text.toPlainText())
            self.update_title()

    def update_title(self):
        current_file = os.path.basename(self.file_name)
        self.setWindowTitle('MandeepPAD - ' + current_file)

    def quit_application(self):
        QApplication.quit()


def main():
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(application.exec_())

main()
