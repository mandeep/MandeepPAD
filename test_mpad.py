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
        coordinates = ['1024', '768']
        assert self.editor.height() == 768
        assert self.editor.width() == 1024
        for coordinate in coordinates:
            assert coordinate in str(self.editor.geometry())

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

    def test_file_name(self):

        assert self.editor.file_name is None
