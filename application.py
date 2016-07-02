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
        """
        QMainWindow constructs the window that contains the text area.
        init_UI() is called here to send the application features to the window.
        """
        QMainWindow.__init__(self, parent)
        self.init_UI()

    def init_UI(self):
        """
        init_UI() contains all of the features of the text editor. These features are
        called by QMainWindow. QTextEdit creates a text area in the main window.
        """
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('MandeepPAD')

        self.menu_bar()
        self.file_menu()

        self.file_name = None

        self.status_bar = self.statusBar()

    def menu_bar(self):
        """
        The menu_bar is initiated here along with each option on the menu bar.
        """
        menu_bar = self.menuBar()
        self.file = menu_bar.addMenu('File')
        self.edit = menu_bar.addMenu('Edit')
        self.preferences = menu_bar.addMenu('Preferences')
        self.help_menu = menu_bar.addMenu('Help')

    def file_menu(self):
        """
        file_menu() contains all of the clickable items inside the file menu.
        Each item is initiated via QAction and called via their own methods
        when triggered. The addAction method sends the actions to the menu_bar().
        """
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
        """
        Creates a new window with an empty text area.
        """
        new_window = TextEditor(self)
        new_window.show()

    def open_file(self):
        """
        Allows for the user to open any file located on their drive.
        When a file is opened, the title is updated to include the filename.
        """
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File')

        if self.file_name:
            with open(self.file_name) as file:
                self.text.setText(file.read())
            self.update_title()

    def save_file(self):
        """
        If the current file does not have a file name, a dialog opens and
        allows the user to save the file to their drive. The title is
        updated to reflect the new filename.
        """
        if not self.file_name:
            self.file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')

        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text.toPlainText())
            self.update_title()

    def update_title(self):
        """
        Uses os.path to retrieve the name of the current file and update
        the window title to include the filename.
        """
        current_file = os.path.basename(self.file_name)
        self.setWindowTitle('MandeepPAD - ' + current_file)

    def quit_application(self):
        """
        Closes the window and quits the application.
        """
        QApplication.quit()


def main():
    """
    QApplication manages the GUI that is initiated by the window variable.
    """
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(application.exec_())

main()
