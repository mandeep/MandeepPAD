import sys
from PyQt5.QtWidgets import QApplication, QTextEdit


application = QApplication(sys.argv)

window = QTextEdit()
window.resize(1024, 768)
window.move(400, 200)
window.setWindowTitle('MandeepPAD')
window.show()

sys.exit(application.exec_())