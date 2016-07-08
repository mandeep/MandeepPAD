import os
import sys
import mpad
import pytest
from PyQt5.QtTest import QTest
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit, QAction,
                             QFileDialog, QFontDialog, QMessageBox, QInputDialog)

app = QApplication(sys.argv)


class TestClass:

    def setup(self):

        self.window = mpad.TextEditor()
        self.window.show()

    def test_window_name(self):
        assert self.window.windowTitle() == 'MandeepPAD'

    def test_geometry(self):
        assert self.window.height() == 768
        assert self.window.width() == 1024

    def test_bars(self):
        assert self.window.statusBar()
        assert self.window.menuBar()
