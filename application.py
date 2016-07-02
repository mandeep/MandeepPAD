import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction, QFileDialog, QFontDialog
from PyQt5.QtGui import QIcon


class TextEditor(QMainWindow):
    """
    TextEditor class houses all of the methods needed to create the
    text editor application. The actual text editor window is initiated
    in the main() function which is called via entrypoint.
    """
    def __init__(self, parent=None):
        """
        QMainWindow constructs the window that contains the text area.
        init_ui() is called here to send the application features to the window.
        """
        QMainWindow.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        """
        Contains all of the features of the text editor. These features are
        called by QMainWindow. QTextEdit creates a text area in the main window.
        """
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('MandeepPAD')
        self.text.setTabStopWidth(50)
        self.setWindowIcon(QIcon('icon.png'))

        self.menu_bar()
        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.preferences_menu()

        self.file_name = None

        self.status_bar = self.statusBar()

    def menu_bar(self):
        """
        The menu bar is initiated here along with each option on the menu bar.
        """
        menu_bar = self.menuBar()
        self.file = menu_bar.addMenu('File')
        self.edit = menu_bar.addMenu('Edit')
        self.view = menu_bar.addMenu('View')
        self.preferences = menu_bar.addMenu('Preferences')
        self.help_menu = menu_bar.addMenu('Help')

    def file_menu(self):
        """
        Contains all of the clickable items inside the file menu.
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

    def edit_menu(self):
        """
        Contains undo, redo, copy, cut, paste, and select all items of the edit menu.
        Each item is initiated via QAction and called via PyQt's text methods
        when triggered. The addAction method sends the actions to the menu_bar().
        """
        self.undoAction = QAction('Undo', self)
        self.undoAction.setStatusTip('Undo last action.')
        self.undoAction.setShortcut('CTRL+Z')
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QAction('Redo', self)
        self.redoAction.setStatusTip('Redo last action.')
        self.redoAction.setShortcut('CTRL+Y')
        self.redoAction.triggered.connect(self.text.redo)

        self.copyAction = QAction('Copy', self)
        self.copyAction.setStatusTip('Copy selected text.')
        self.copyAction.setShortcut('CTRL+C')
        self.copyAction.triggered.connect(self.text.copy)

        self.cutAction = QAction('Cut', self)
        self.cutAction.setStatusTip('Cut selected text.')
        self.cutAction.setShortcut('CTRL+X')
        self.cutAction.triggered.connect(self.text.cut)

        self.pasteAction = QAction('Paste', self)
        self.pasteAction.setStatusTip('Paste copied text.')
        self.pasteAction.setShortcut('CTRL+V')
        self.pasteAction.triggered.connect(self.text.paste)

        self.selectAction = QAction('Select all', self)
        self.selectAction.setStatusTip('Select all text.')
        self.selectAction.setShortcut('CTRL+A')
        self.selectAction.triggered.connect(self.text.selectAll)

        self.edit.addAction(self.undoAction)
        self.edit.addAction(self.redoAction)
        self.edit.addAction(self.copyAction)
        self.edit.addAction(self.cutAction)
        self.edit.addAction(self.pasteAction)
        self.edit.addAction(self.selectAction)

    def view_menu(self):
        """
        Items that allow the user to change the design of the application.
        """
        self.menu_barAction = QAction('Toggle menu bar', self)
        self.menu_barAction.setStatusTip('Toggle the visibility of the menu bar.')
        self.menu_barAction.triggered.connect(self.menu_bar_visibility)

        self.status_barAction = QAction('Toggle status bar', self)
        self.status_barAction.setStatusTip('Toggle the visibility of the status bar.')
        self.status_barAction.triggered.connect(self.status_bar_visibility)

        self.view.addAction(self.menu_barAction)
        self.view.addAction(self.status_barAction)

    def preferences_menu(self):
        """
        Contains items that allow the user to change the text area options.
        """
        self.font_familyAction = QAction('Font family', self)
        self.font_familyAction.setStatusTip('Change the current font.')
        self.font_familyAction.triggered.connect(self.change_font)

        self.preferences.addAction(self.font_familyAction)

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
        self.setWindowTitle('MandeepPAD - {}' .format(current_file))

    def menu_bar_visibility(self):
        """
        Allows the user to set the visibility of the menu bar.
        """
        if self.menuBar().isVisible():
            self.menuBar().setVisible(False)
        else:
            self.menuBar().setVisible(True)

    def status_bar_visibility(self):
        """
        Allows the user to specify the visibility of the status bar.
        """
        if self.status_bar.isVisible():
            self.status_bar.setVisible(False)
        else:
            self.status_bar.setVisible(True)

    def change_font(self):
        """
        Allows the user to change the font family, style and size.
        """
        font, selected = QFontDialog.getFont()
        if selected:
            self.text.setFont(font)

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
