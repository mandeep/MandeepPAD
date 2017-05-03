import os
import pkg_resources
import time
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QFileDialog,
                             QFontDialog, QInputDialog, QMainWindow,
                             QMessageBox, QPlainTextEdit, QToolBar)


class TextEditor(QMainWindow):
    """
    TextEditor class houses all of the methods needed to create the
    text editor application. The actual text editor window is initiated
    in the main() function which is called via entrypoint.
    """
    def __init__(self, parent=None):
        """
        QMainWindow constructs the window that contains the text area.
        init_ui() is called here to send the application's UI
        elements to the main window.
        """
        QMainWindow.__init__(self, parent)

        self.text = QPlainTextEdit(self)
        self.setCentralWidget(self.text)

        self.resize(800, 700)
        self.setWindowTitle('MandeepPAD')
        self.text.setTabStopWidth(50)
        self.text.setFont(QFont("Source Code Pro"))
        window_icon = pkg_resources.resource_filename('mpad.images', 'icon.png')
        self.setWindowIcon(QIcon(window_icon))

        self.status_bar = self.statusBar()
        self.tool_bar()

        self.menu_bar_item()
        self.file_menu()
        self.edit_menu()
        self.format_menu()
        self.tools_menu()
        self.view_menu()
        self.help_menu()

        self.file_name = None

    def menu_bar_item(self):
        """Initiate the menubar along with each of its items."""
        self.menu_bar = self.menuBar()
        self.file = self.menu_bar.addMenu('File')
        self.edit = self.menu_bar.addMenu('Edit')
        self.form = self.menu_bar.addMenu('Format')
        self.tools = self.menu_bar.addMenu('Tools')
        self.view = self.menu_bar.addMenu('View')
        self.help_option = self.menu_bar.addMenu('Help')

    def file_menu(self):
        """Initiate each of the items in the File submenu."""
        self.new_action = QAction('New File', self)
        self.new_action.setStatusTip('Create a new document.')
        self.new_action.setShortcut('CTRL+N')
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction('Open File', self)
        self.open_action.setStatusTip('Open an existing document.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction('Save File', self)
        self.save_action.setStatusTip('Save the current document.')
        self.save_action.setShortcut('CTRL+S')
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction('Save File As', self)
        self.save_as_action.setStatusTip('Save the current document as a new file.')
        self.save_as_action.setShortcut('CTRL+SHIFT+S')
        self.save_as_action.triggered.connect(self.save_file_as)

        self.print_action = QAction('Print', self)
        self.print_action.setStatusTip('Print the current document.')
        self.print_action.setShortcut('CTRL+P')
        self.print_action.triggered.connect(self.print_file)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setStatusTip('Quit application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file.addAction(self.new_action)
        self.file.addAction(self.open_action)
        self.file.addAction(self.save_action)
        self.file.addAction(self.save_as_action)
        self.file.addSeparator()
        self.file.addAction(self.print_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """Initiate items that allow the user to edit the current document."""
        self.undo_action = QAction('Undo', self)
        self.undo_action.setStatusTip('Undo last action.')
        self.undo_action.setShortcut('CTRL+Z')
        self.undo_action.triggered.connect(self.text.undo)

        self.redo_action = QAction('Redo', self)
        self.redo_action.setStatusTip('Redo last action.')
        self.redo_action.setShortcut('CTRL+Y')
        self.redo_action.triggered.connect(self.text.redo)

        self.copy_action = QAction('Copy', self)
        self.copy_action.setStatusTip('Copy selected text.')
        self.copy_action.setShortcut('CTRL+C')
        self.copy_action.triggered.connect(self.text.copy)

        self.cut_action = QAction('Cut', self)
        self.cut_action.setStatusTip('Cut selected text.')
        self.cut_action.setShortcut('CTRL+X')
        self.cut_action.triggered.connect(self.text.cut)

        self.paste_action = QAction('Paste', self)
        self.paste_action.setStatusTip('Paste copied text.')
        self.paste_action.setShortcut('CTRL+V')
        self.paste_action.triggered.connect(self.text.paste)

        self.delete_action = QAction('Delete', self)
        self.delete_action.setStatusTip('Delete selected text.')
        self.delete_action.triggered.connect(self.delete_text)

        self.select_action = QAction('Select All', self)
        self.select_action.setStatusTip('Select all text.')
        self.select_action.setShortcut('CTRL+A')
        self.select_action.triggered.connect(self.text.selectAll)

        self.edit.addAction(self.undo_action)
        self.edit.addAction(self.redo_action)
        self.edit.addSeparator()
        self.edit.addAction(self.copy_action)
        self.edit.addAction(self.cut_action)
        self.edit.addAction(self.paste_action)
        self.edit.addAction(self.delete_action)
        self.edit.addSeparator()
        self.edit.addAction(self.select_action)

    def format_menu(self):
        """Initiate items that allow the user to change the format of the text."""
        self.font_family_action = QAction('Font', self)
        self.font_family_action.setStatusTip('Change the current font.')
        self.font_family_action.triggered.connect(self.change_font)

        self.form.addAction(self.font_family_action)

    def tools_menu(self):
        """Initialize items that allow the user to enhance their text experience."""
        self.find_action = QAction('Find Text', self)
        self.find_action.setStatusTip('Find text within the document.')
        self.find_action.setShortcut('CTRL+F')
        self.find_action.triggered.connect(self.text_search)

        self.find_next_action = QAction('Find Next', self)
        self.find_next_action.setStatusTip('Find the next occurrence of the selected text.')
        self.find_next_action.setShortcut('F3')
        self.find_next_action.triggered.connect(self.find_next_text)

        self.char_count_action = QAction('Character Count', self)
        self.char_count_action.setStatusTip('View the number of characters in the document.')
        self.char_count_action.triggered.connect(self.char_count)

        self.word_count_action = QAction('Word Count', self)
        self.word_count_action.setStatusTip('View the number of words in the selection.')
        self.word_count_action.triggered.connect(self.word_count)

        self.date_action = QAction('Insert Date/Time', self)
        self.date_action.setStatusTip('Add a date and time to the document.')
        self.date_action.triggered.connect(self.insert_date)

        self.tools.addAction(self.find_action)
        self.tools.addAction(self.find_next_action)
        self.tools.addSeparator()
        self.tools.addAction(self.date_action)
        self.tools.addSeparator()
        self.tools.addAction(self.char_count_action)
        self.tools.addAction(self.word_count_action)

    def view_menu(self):
        """Initiate items that allow the user to change the design of the application."""
        self.menu_bar_action = QAction('Hide Menubar', self)
        self.menu_bar_action.setStatusTip('Hide the menubar.')
        self.menu_bar_action.triggered.connect(self.menu_bar_visibility)

        self.tool_bar_action = QAction('Show Toolbar', self)
        self.tool_bar_action.setStatusTip('Show the toolbar.')
        self.tool_bar_action.triggered.connect(self.tool_bar_visibility)

        self.status_bar_action = QAction('Hide Statusbar', self)
        self.status_bar_action.setStatusTip('Hide the status bar.')
        self.status_bar_action.triggered.connect(self.status_bar_visibility)

        self.view.addAction(self.menu_bar_action)
        self.view.addAction(self.tool_bar_action)
        self.view.addAction(self.status_bar_action)

    def help_menu(self):
        """Contains informative items for the user."""
        self.about_action = QAction('About', self)
        self.about_action.setStatusTip('About application.')
        self.about_action.triggered.connect(self.about)

        self.help_option.addAction(self.about_action)

    def tool_bar(self):
        """Create a toolbar underneath the menu bar with common items such as new
        document, open document, save document, etc.
        """
        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.hide()

        new_window_icon = pkg_resources.resource_filename('mpad.images', 'document_icon.png')
        new_window = QAction(QIcon(new_window_icon), 'New window', self)
        new_window.triggered.connect(self.new_file)

        open_document_icon = pkg_resources.resource_filename('mpad.images', 'doc_import_icon.png')
        open_document = QAction(QIcon(open_document_icon), 'Open document', self)
        open_document.triggered.connect(self.open_file)

        save_document_icon = pkg_resources.resource_filename('mpad.images', 'save_icon.png')
        save_document = QAction(QIcon(save_document_icon), 'Save document', self)
        save_document.triggered.connect(self.save_file)

        copy_text_icon = pkg_resources.resource_filename('mpad.images', 'clipboard_copy_icon.png')
        copy_text = QAction(QIcon(copy_text_icon), 'Copy text', self)
        copy_text.triggered.connect(self.text.copy)

        cut_text_icon = pkg_resources.resource_filename('mpad.images', 'clipboard_cut_icon.png')
        cut_text = QAction(QIcon(cut_text_icon), 'Cut text', self)
        cut_text.triggered.connect(self.text.cut)

        paste_text_icon = pkg_resources.resource_filename('mpad.images', 'clipboard_paste_icon.png')
        paste_text = QAction(QIcon(paste_text_icon), 'Paste text', self)
        paste_text.triggered.connect(self.text.paste)

        select_all_icon = pkg_resources.resource_filename('mpad.images', 'doc_lines_icon.png')
        select_all = QAction(QIcon(select_all_icon), 'Select all', self)
        select_all.triggered.connect(self.text.selectAll)

        find_icon = pkg_resources.resource_filename('mpad.images', 'find_icon.png')
        find_in_text = QAction(QIcon(find_icon), 'Find text', self)
        find_in_text.triggered.connect(self.text_search)

        self.toggle_menu_bar = QAction(QIcon().fromTheme('document-revert'), 'Show menu bar', self)
        self.toggle_menu_bar.triggered.connect(self.menu_bar_visibility)

        self.toolbar.addAction(new_window)
        self.toolbar.addAction(open_document)
        self.toolbar.addAction(save_document)
        self.toolbar.addAction(copy_text)
        self.toolbar.addAction(cut_text)
        self.toolbar.addAction(paste_text)
        self.toolbar.addAction(select_all)
        self.toolbar.addAction(find_in_text)

    def new_file(self):
        """Create a new window with an empty text area."""
        new_window = TextEditor(self)
        new_window.show()

    def open_file(self):
        """Open an existing document."""
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File')

        if self.file_name:
            with open(self.file_name) as file:
                self.text.setPlainText(file.read())
            self.update_title()

    def save_file(self):
        """Save the current document.

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

    def save_file_as(self):
        """Save the current document as a new file."""
        self.file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')

        with open(self.file_name, 'w') as file:
            file.write(self.text.toPlainText())
        self.update_title()

    def print_file(self):
        """Print the current document to the selected printer."""
        print_dialog = QPrintDialog()
        if print_dialog.exec_() == QDialog.Accepted:
            self.text.print(print_dialog.printer())

    def update_title(self):
        """Update the window title to show the name of the current document."""
        current_file = os.path.basename(self.file_name)
        self.setWindowTitle('MandeepPAD - {}' .format(current_file))

    def delete_text(self):
        """Delete the text in the current selection."""
        cursor = self.text.textCursor()
        cursor.removeSelectedText()

    def change_font(self):
        """Open a font dialog that allows the user to change the font family, style and size."""
        font, selected = QFontDialog.getFont(self)
        if selected:
            self.text.setFont(font)

    def text_search(self):
        """Search the document for the text given by the user from the input dialog. 

        If there is no current selection, the cursor is moved to the
        beginning of the document before starting the search. If there is a
        current selection, the search returns text located after the
        selected text.
        """
        find_text, ok = QInputDialog.getText(self, 'Find text', 'Enter text to find:')

        if ok and not self.text.textCursor().hasSelection():
            self.text.moveCursor(1)
            self.text.find(find_text)
        else:
            self.text.find(find_text)

    def find_next_text(self):
        """Find the next occurrence of the selected text.

        May be used with the 'Find Text' dialog or as a standalone action.
        """
        if self.text.textCursor().hasSelection():
            selected_text = self.text.textCursor().selectedText()
            self.text.find(selected_text)

    def char_count(self):
        """Find the length of all of the text in the document."""
        cursor = self.text.textCursor()
        character_message = QMessageBox()
        character_message.setWindowTitle('Character count')
        character_message.setText('Total characters in document:')
        character_message.setInformativeText("{:,}" .format(cursor.position()))
        character_message.exec_()

    def word_count(self):
        """Find the number of words in the document.

        The entire text in the document is automatically selected.
        Next the text is split into a list by using spaces as a separator.
        The length of the list is returned as a string in a message box.
        """
        cursor = self.text.textCursor()
        cursor.select(3)
        word_count_message = QMessageBox()
        word_count_message.setWindowTitle('Word count')
        word_count_message.setText('Total words in document:')
        number_of_words = len(cursor.selectedText().split())
        word_count_message.setInformativeText("{:,}" .format(number_of_words))
        word_count_message.exec_()

    def insert_date(self):
        """Insert the current date and time in the format of YYYY-MM-DD HH:mm:ss.

        Example: 2017-04-04 22:21:01. The time zone retrieved defaults to
        the current user's time zone.
        """
        cursor = self.text.textCursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.insertText(current_time)

    def menu_bar_visibility(self):
        """Set the visibility of the menu bar.

        When the menu bar is toggled off, an icon is placed on the tool bar
        to allow the user to show the menu bar again.
        """
        if self.menu_bar.isVisible():
            self.menu_bar.setVisible(False)
            self.toolbar.addAction(self.toggle_menu_bar)
        else:
            self.menu_bar.setVisible(True)
            self.toolbar.removeAction(self.toggle_menu_bar)

    def status_bar_visibility(self):
        """Set the visibility of the status bar."""
        if self.status_bar.isVisible():
            self.status_bar.setVisible(False)
            self.status_bar_action.setText('Show Statusbar')
        else:
            self.status_bar.setVisible(True)
            self.status_bar_action.setText('Hide Statusbar')

    def tool_bar_visibility(self):
        """Set the visibility of the toolbar."""
        if self.toolbar.isVisible():
            self.toolbar.hide()
            self.tool_bar_action.setText('Show Toolbar')
            self.tool_bar_action.setStatusTip('Show the tool bar.')
        else:
            self.toolbar.show()
            self.tool_bar_action.setText('Hide Toolbar')
            self.tool_bar_action.setStatusTip('Hide the tool bar.')

    @staticmethod
    def about():
        """Display a dialog with details of the application."""
        message = QMessageBox()
        message.setWindowTitle('MandeepPAD')
        message_icon = pkg_resources.resource_filename('mpad.images', 'md_help.png')
        message.setWindowIcon(QIcon(message_icon))
        message.setText('Created by Mandeep')
        message.setInformativeText('GitHub: mandeep')
        message.exec_()


def main():
    """QApplication manages the GUI that is initiated by the window variable."""
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as file:
            window.text.setPlainText(file.read())
            window.setWindowTitle('MandeepPAD - {}' .format(sys.argv[1]))
    sys.exit(application.exec_())
