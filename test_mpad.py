import os
import sys
import mpad
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QFontDialog, QMessageBox, QInputDialog)

app = QApplication(sys.argv)


class TestClass:

    def setup(self):
        self.editor = mpad.TextEditor()
        self.editor.show()

    def test_window_name(self):
        assert self.editor.windowTitle() == 'MandeepPAD'

    def test_geometry(self):
        assert self.editor.height() == 768
        assert self.editor.width() == 1024

    def test_bars(self):
        """
        Tests whether the widget contains a status bar and menu bar.
        """
        assert self.editor.statusBar()
        assert self.editor.menuBar()

    def test_menu_bar(self):
        """
        Tests whether the menu items appear on the menu bar.
        """
        assert self.editor.file
        assert self.editor.edit
        assert self.editor.form
        assert self.editor.tools
        assert self.editor.view
        assert self.editor.help_option

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
