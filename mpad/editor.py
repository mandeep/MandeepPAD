import arrow
import os
import pkg_resources
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QFontDialog, QMessageBox,
                             QInputDialog, QToolBar)
import sys


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
        self.init_ui()

    def init_ui(self):
        """
        Contains all of the UI elements of the text editor. These elements are
        sent to QMainWindow. QTextEdit creates a text area in the main window.
        """
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(400, 200, 1024, 768)
        self.setWindowTitle('MandeepPAD')
        self.text.setTabStopWidth(50)
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
        """
        The menu bar is initiated here along with each option on the menu bar.
        """
        self.menu_bar = self.menuBar()
        self.file = self.menu_bar.addMenu('File')
        self.edit = self.menu_bar.addMenu('Edit')
        self.form = self.menu_bar.addMenu('Format')
        self.tools = self.menu_bar.addMenu('Tools')
        self.view = self.menu_bar.addMenu('View')
        self.help_option = self.menu_bar.addMenu('Help')

    def file_menu(self):
        """
        Contains all of the clickable items inside the file menu.
        Each item is initiated via QAction and called via their own methods
        when triggered. The addAction method sends the actions to the
        menu_bar().
        """
        self.new_action = QAction('New file', self)
        self.new_action.setStatusTip('Create a new document.')
        self.new_action.setShortcut('CTRL+N')
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction('Open file', self)
        self.open_action.setStatusTip('Open an existing document.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction('Save file', self)
        self.save_action.setStatusTip('Save the current document.')
        self.save_action.setShortcut('CTRL+S')
        self.save_action.triggered.connect(self.save_file)

        self.print_action = QAction('Print', self)
        self.print_action.setStatusTip('Print the current document.')
        self.print_action.setShortcut('CTRL+P')
        self.print_action.triggered.connect(self.print_file)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setStatusTip('Quit application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(self.quit_application)

        self.file.addAction(self.new_action)
        self.file.addAction(self.open_action)
        self.file.addAction(self.save_action)
        self.file.addSeparator()
        self.file.addAction(self.print_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """
        Contains undo, redo, copy, cut, paste, and select all items of the
        edit menu. Each item is initiated via QAction and called via PyQt's
        text methods when triggered. The addAction method sends the actions
        to the menu_bar().
        """
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

        self.select_action = QAction('Select all', self)
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
        """
        Contains items that allow the user to change the format of the text.
        """
        self.font_family_action = QAction('Font', self)
        self.font_family_action.setStatusTip('Change the current font.')
        self.font_family_action.triggered.connect(self.change_font)

        self.bold_action = QAction('Bold', self)
        self.bold_action.setStatusTip('Change the font weight to bold.')
        self.bold_action.setShortcut('CTRL+B')
        self.bold_action.triggered.connect(self.bolden)

        self.italic_action = QAction('Italic', self)
        self.italic_action.setStatusTip('Change the font style to italic.')
        self.italic_action.setShortcut('CTRL+I')
        self.italic_action.triggered.connect(self.italicize)

        self.underline_action = QAction('Underline', self)
        self.underline_action.setStatusTip('Add an underline to the font.')
        self.underline_action.setShortcut('CTRL+U')
        self.underline_action.triggered.connect(self.underliner)

        self.form.addAction(self.font_family_action)
        self.form.addSeparator()
        self.form.addAction(self.bold_action)
        self.form.addAction(self.italic_action)
        self.form.addAction(self.underline_action)

    def view_menu(self):
        """
        Items that allow the user to change the design of the application.
        """

        self.menu_bar_action = QAction('Hide menu bar', self)
        self.menu_bar_action.setStatusTip('Hide the menu bar.')
        self.menu_bar_action.triggered.connect(self.menu_bar_visibility)

        self.status_bar_action = QAction('Hide status bar', self)
        self.status_bar_action.setStatusTip('Hide the status bar.')
        self.status_bar_action.triggered.connect(self.status_bar_visibility)

        self.tool_bar_action = QAction('Hide tool bar', self)
        self.tool_bar_action.setStatusTip('Hide the tool bar.')
        self.tool_bar_action.triggered.connect(self.tool_bar_visibility)

        self.view.addAction(self.menu_bar_action)
        self.view.addAction(self.tool_bar_action)
        self.view.addAction(self.status_bar_action)

    def tools_menu(self):
        """
        Contains items that allow the user to enhance their text experience.
        """
        self.find_action = QAction('Find text', self)
        self.find_action.setStatusTip('Find text within the document.')
        self.find_action.setShortcut('CTRL+F')
        self.find_action.triggered.connect(self.text_search)

        self.find_next_action = QAction('Find next', self)
        self.find_next_action.setStatusTip('Find the next occurrence of the selected text.')
        self.find_next_action.setShortcut('F3')
        self.find_next_action.triggered.connect(self.find_next_text)

        self.char_count_action = QAction('Character count', self)
        self.char_count_action.setStatusTip('View the number of characters in the document.')
        self.char_count_action.triggered.connect(self.char_count)

        self.word_count_action = QAction('Word count', self)
        self.word_count_action.setStatusTip('View the number of words in the selection.')
        self.word_count_action.triggered.connect(self.word_count)

        self.date_action = QAction('Insert date/time', self)
        self.date_action.setStatusTip('Add a date and time to the document.')
        self.date_action.triggered.connect(self.insert_date)

        self.tools.addAction(self.find_action)
        self.tools.addAction(self.find_next_action)
        self.tools.addSeparator()
        self.tools.addAction(self.date_action)
        self.tools.addSeparator()
        self.tools.addAction(self.char_count_action)
        self.tools.addAction(self.word_count_action)

    def help_menu(self):
        """
        Contains informative items for the user.
        """
        self.about_action = QAction('About', self)
        self.about_action.setStatusTip('About application.')
        self.about_action.triggered.connect(self.about)

        self.help_option.addAction(self.about_action)

    def tool_bar(self):
        """
        Creates a toolbar underneath the menu bar with common items such as new
        document, open document, save document, etc.
        """
        self.toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

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
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open file')

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
            self.file_name, _ = QFileDialog.getSaveFileName(self, 'Save file')

        if self.file_name:
            with open(self.file_name, 'w') as file:
                file.write(self.text.toPlainText())
            self.update_title()

    def print_file(self):
        """
        Opens print dialog that allows the user to change the print settings
        as well as print the document.
        """
        print_dialog = QPrintDialog()
        print_dialog.printer()
        print_dialog.exec_()

    def update_title(self):
        """
        Uses os.path to retrieve the name of the current file and update
        the window title to include the filename.
        """
        current_file = os.path.basename(self.file_name)
        self.setWindowTitle('MandeepPAD - {}' .format(current_file))

    def delete_text(self):
        """
        Deletes the text in the current selection.
        """
        cursor = self.text.textCursor()
        cursor.removeSelectedText()

    def change_font(self):
        """
        Opens a font dialog that allows the user to change the font family,
        style and size.
        """
        font, selected = QFontDialog.getFont(self)
        if selected:
            self.text.setFont(font)

    def bolden(self):
        """
        Boldens the text that is to be written in the document.
        """
        if self.text.fontWeight() == 50:
            self.text.setFontWeight(75)
        else:
            self.text.setFontWeight(50)

    def italicize(self):
        """
        Italicizes the text that is to be written in the document.
        """
        if not self.text.fontItalic():
            self.text.setFontItalic(True)
        else:
            self.text.setFontItalic(False)

    def underliner(self):
        """
        Adds an underline to the text that is to be written in the document.
        """
        if not self.text.fontUnderline():
            self.text.setFontUnderline(True)
        else:
            self.text.setFontUnderline(False)

    def text_search(self):
        """
        Searches the document for the text given by the user from the input
        dialog. If there is no current selection, the cursor is moved to the
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
        """
        Finds the next occurrence of the selected text. Can be used with the
        'Find text' dialog or as a standalone action.
        """
        if self.text.textCursor().hasSelection():
            selected_text = self.text.textCursor().selectedText()
            self.text.find(selected_text)

    def char_count(self):
        """
        Finds the length of all of the text in the document via
        QTextEdit().textCursor().position() and returns it as a string
        in a message box.
        """
        cursor = self.text.textCursor()
        character_message = QMessageBox()
        character_message.setWindowTitle('Character count')
        character_message.setText('Total characters in document:')
        character_message.setInformativeText(str(cursor.position()))
        character_message.exec_()

    def word_count(self):
        """
        Finds the number of words in the document with use of the
        textCursor() method of QTextEdit. The entire text in the document
        is automatically selected. Next the text is split into a list by
        using spaces as a separator. The length of the list is returned
        as a string in a message box.
        """
        cursor = self.text.textCursor()
        cursor.select(3)
        word_count_message = QMessageBox()
        word_count_message.setWindowTitle('Word count')
        word_count_message.setText('Total words in document:')
        number_of_words = len(cursor.selectedText().split())
        word_count_message.setInformativeText(str(number_of_words))
        word_count_message.exec_()

    def insert_date(self):
        """
        Inserts the current date and time in the format of YYYY-MM-DD HH:mm:ss.
        Example: 2016-07-14 15:39:01. The time zone retrieved defaults to
        the current user's time zone.
        """
        cursor = self.text.textCursor()
        time = arrow.now().format('YYYY-MM-DD HH:mm:ss')
        cursor.insertText(time)

    def menu_bar_visibility(self):
        """
        Allows the user to set the visibility of the menu bar. When the menu
        bar is toggled off, an icon is placed on the tool bar to allow the user
        to show the menu bar again.
        """
        if self.menu_bar.isVisible():
            self.menu_bar.setVisible(False)
            self.toolbar.addAction(self.toggle_menu_bar)
        else:
            self.menu_bar.setVisible(True)
            self.toolbar.removeAction(self.toggle_menu_bar)

    def status_bar_visibility(self):
        """
        Allows the user to specify the visibility of the status bar.
        """
        if self.status_bar.isVisible():
            self.status_bar.setVisible(False)
            self.status_bar_action.setText('Show status bar')
        else:
            self.status_bar.setVisible(True)
            self.status_bar_action.setText('Hide status bar')

    def tool_bar_visibility(self):
        """
        Allows the user to specify the visibility of the tool bar.
        """
        if self.toolbar.isVisible():
            self.toolbar.hide()
            self.tool_bar_action.setText('Show tool bar')
            self.tool_bar_action.setStatusTip('Show the tool bar.')
        else:
            self.toolbar.show()
            self.tool_bar_action.setText('Hide tool bar')
            self.tool_bar_action.setStatusTip('Hide the tool bar.')

    def about(self):
        """
        Shows the user a popup box with details of the application.
        """
        message = QMessageBox()
        message.setWindowTitle('MandeepPAD')
        message_icon = pkg_resources.resource_filename('mpad.images', 'md_help.png')
        message.setWindowIcon(QIcon(message_icon))
        message.setText('Created by Mandeep Bhutani')
        message.setInformativeText('GitHub: mandeepbhutani')
        message.exec_()

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
