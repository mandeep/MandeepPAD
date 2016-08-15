from mpad import editor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QFontDialog, QMessageBox, QInputDialog, QWidget)
import sys

app = QApplication(sys.argv)


class TestClass:

    def setup(self):
        self.editor = editor.TextEditor()
        self.editor.show()

    def test_window(self):
        assert self.editor.windowTitle() == 'MandeepPAD'
        assert self.editor.windowIcon().isNull() is False

    def test_geometry(self):
        assert self.editor.width() == 1024
        assert self.editor.height() == 768

    def test_text_area(self):
        sentence = 'They gave my red hat to the donkey.'
        cursor = self.editor.text.textCursor()
        cursor.insertText(sentence)
        cursor.select(3)
        assert cursor.selectedText() == sentence
        assert self.editor.text.tabStopWidth() == 50

    def test_bars(self):
        """Tests whether the widget contains a status bar and menu bar.
        """
        assert self.editor.statusBar().isVisible()
        assert self.editor.menuBar().isVisible()

    def test_menu_bar(self):
        """Tests whether the menu items appear on the menu bar.
        """
        assert self.editor.file.isEnabled()
        assert self.editor.edit.isEnabled()
        assert self.editor.form.isEnabled()
        assert self.editor.tools.isEnabled()
        assert self.editor.view.isEnabled()
        assert self.editor.help_option.isEnabled()

    def test_new_file(self, qtbot):
        """Qtbot simulates clicks inside the text editor window to ensure
        that a new window opens when New File is selected.
        """
        qtbot.mouseClick(self.editor.file, Qt.LeftButton)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Enter)

    def test_open_file(self, qtbot, mock):
        """Qtbot simulates clicks inside the text editor window to ensure
        that an open file dialog opens when Open File is selected."""
        qtbot.mouseClick(self.editor.file, Qt.LeftButton)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('.travis.yml', '*.txt'))
        self.editor.open_file()

    def test_save_file(self, qtbot, mock):
        """Qtbot simulates clicks inside the text editor window to ensure
        that a save file dialog opens when Save File is selected."""
        qtbot.mouseClick(self.editor.file, Qt.LeftButton)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getSaveFileName', return_value=('.travis.yml', '*.txt'))
        self.editor.save_file()

    def test_print_file(self, qtbot, mock):
        """Qtbot simulates clicks inside the text editor window to ensure
        that a save file dialog opens when Save File is selected."""
        qtbot.mouseClick(self.editor.file, Qt.LeftButton)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        mock.patch.object(QPrintDialog, 'exec_', return_value='accept')
        qtbot.keyClick(self.editor.file, Qt.Key_Enter)

    def test_quit_application(self, qtbot, monkeypatch):
        """Qtbot scolls through menu items and monkeypatch intercepts the quit
        application call prior to it being called."""
        exit_calls = []
        monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Down)
        qtbot.keyClick(self.editor.file, Qt.Key_Enter)
        assert exit_calls == [1]

    def test_undo_action(self, qtbot):
        """Inserts text into the text area then qtbot navigates to Undo
        and selects it.
        """
        sentence = "My back. There goes my back again."
        cursor = self.editor.text.textCursor()
        cursor.insertText(sentence)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)
        cursor.select(3)
        assert cursor.selectedText() is ''

    def test_redo_action(self, qtbot):
        """Inserts text into the text area then qtbot navigates to Undo
        and selects it. Qtbot  then navigates to the redo action and
        selects it.
        """
        sentence = "Oh, hello, Principal Skinner. I'd get up, but the boy crippled me."
        cursor = self.editor.text.textCursor()
        cursor.insertText(sentence)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)
        cursor.select(3)
        assert cursor.selectedText() == sentence

    def test_delete_action(self, qtbot):
        """Inserts text into the text area then qtbot navigates to Delete
        and selects it.
        """
        sentence = "Go get help, Dog."
        cursor = self.editor.text.textCursor()
        cursor.insertText(sentence)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)

    def test_select_all(self, qtbot):
        """Inserts text into the text area then qtbot navigates to the Select
        All item and seelcts it."""
        sentence = "Oh, the boy. Bring me the boy."
        cursor = self.editor.text.textCursor()
        cursor.insertText(sentence)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)

    def test_font_dialog(self, qtbot, mock):
        """Qtbot opens the format menu and selects the Change Font item."""
        qtbot.mouseClick(self.editor.form, Qt.LeftButton)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        mock.patch.object(QFontDialog, 'getFont', return_value=('', ''))
        qtbot.keyClick(self.editor.form, Qt.Key_Enter)

    def test_bold_font(self, qtbot):
        """Qtbot opens the format menu and selects the Bold item."""
        qtbot.mouseClick(self.editor.form, Qt.LeftButton)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)

    def test_italic_font(self, qtbot):
        """Qtbot opens the format menu and selects the Italicize item."""
        qtbot.mouseClick(self.editor.form, Qt.LeftButton)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)

    def test_underline_font(self, qtbot):
        """Qtbot opens the format menu and selects the Underline item."""
        qtbot.mouseClick(self.editor.form, Qt.LeftButton)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.form, Qt.Key_Down)
        qtbot.keyClick(self.editor.edit, Qt.Key_Enter)

    def test_text_search(self, qtbot, mock):
        """Qtbot opens the tools menu and selects the Find text item."""
        qtbot.mouseClick(self.editor.tools, Qt.LeftButton)
        qtbot.keyClick(self.editor.tools, Qt.Key_Down)
        mock.patch.object(QInputDialog, 'getText', return_value=('Hi!', True))
        qtbot.keyClick(self.editor.tools, Qt.Key_Enter)