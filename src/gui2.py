import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QMenuBar, QStatusBar, QMenu, QAction, QFileDialog
import logics


class UiMainWindow(object):
    logics = None

    def __init__(self):
        self.status_bar = None
        self.menu_file = None
        self.menubar = None
        self.central_widget = None
        self.actionOpen = None
        self.logics = logics.Logics()

    def setup_ui(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 32))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menufile")
        MainWindow.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.status_bar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.actionOpen)

        self.retranslate_ui(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.actionOpen.triggered.connect(lambda: self.get_file())

    # setupUi

    def retranslate_ui(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EDA", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        # if QT_CONFIG(statustip)
        self.actionOpen.setStatusTip(QCoreApplication.translate("MainWindow", u"Open an abf file", None))
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        # endif // QT_CONFIG(shortcut)
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))

    # retranslateUi

    def get_file(self):
        f_name, _ = QFileDialog.getOpenFileName(self.central_widget, 'Open file',
                                                filter="Abf files (*.abf);; Edh files(*.edh)")
        self.logics.open_abf(f_name)
        # print last abf read
        print(self.logics.abfs[len(self.logics.abfs)-1])
        print(len(self.logics.abfs))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    app.exec_()
