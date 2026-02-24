import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from UI.widgets import DataAnalysisWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Microsoft YaHei", 10))

    win = DataAnalysisWindow()
    win.show()

    sys.exit(app.exec_())