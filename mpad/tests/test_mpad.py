from mpad import editor
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QFontDialog, QMessageBox, QInputDialog)
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
        """
        Tests whether the widget contains a status bar and menu bar.
        """
        assert self.editor.statusBar().isVisible()
        assert self.editor.menuBar().isVisible()

    def test_menu_bar(self):
        """
        Tests whether the menu items appear on the menu bar.
        """
        assert self.editor.file.isEnabled()
        assert self.editor.edit.isEnabled()
        assert self.editor.form.isEnabled()
        assert self.editor.tools.isEnabled()
        assert self.editor.view.isEnabled()
        assert self.editor.help_option.isEnabled()

    def test_menu_items(self, qtbot):
        """
        Qtbot simulates mouse clicks inside the text editor window to ensure
        that the items on the menu bar are clickable.
        """
        qtbot.mouseClick(self.editor.file, Qt.LeftButton)
        qtbot.mouseClick(self.editor.edit, Qt.LeftButton)
        qtbot.mouseClick(self.editor.form, Qt.LeftButton)
        qtbot.mouseClick(self.editor.tools, Qt.LeftButton)
        qtbot.mouseClick(self.editor.view, Qt.LeftButton)
        qtbot.mouseClick(self.editor.help_option, Qt.LeftButton)
