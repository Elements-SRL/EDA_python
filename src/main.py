import sys
from PyQt5 import QtWidgets
from main_window import UiMainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(mw)
    mw.show()
    sys.exit(app.exec_())
