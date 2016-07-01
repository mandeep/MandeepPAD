import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit


class TextEditor(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('MandeepPAD')
        self.move(400, 200)

        self.initMenuBar()
        self.statusbar = self.statusBar()

    def initMenuBar(self):
        menubar = self.menuBar()
        file = menubar.addMenu('File')
        edit = menubar.addMenu('Edit')
        preferences = menubar.addMenu('Preferences')
        help_menu = menubar.addMenu('Help')


def main():
    application = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(application.exec_())

main()
