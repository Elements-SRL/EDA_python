import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QMenuBar, QStatusBar, QMenu, QAction, QFileDialog, QGridLayout, QFrame
import logics


class UiMainWindow(object):
    logics = None

    def __init__(self):
        self.menu_export_as = None
        self.frame = None
        self.frame_2 = None
        self.gridLayout = None
        self.action_csv = None
        self.status_bar = None
        self.menu_file = None
        self.menubar = None
        self.central_widget = None
        self.actionOpen = None
        self.logics = logics.Logics()

    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(800, 600)
        self.actionOpen = QAction(main_window)
        self.actionOpen.setObjectName(u"actionOpen")
        self.action_csv = QAction(main_window)
        self.action_csv.setObjectName(u"action_csv")
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(self.central_widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(self.central_widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 722, 32))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menufile")
        self.menu_export_as = QMenu(self.menu_file)
        self.menu_export_as.setObjectName(u"menuExport_as")
        main_window.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.status_bar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.actionOpen)
        self.menu_file.addAction(self.menu_export_as.menuAction())
        self.menu_export_as.addAction(self.action_csv)

        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.actionOpen.triggered.connect(lambda: self.open())
        self.action_csv.triggered.connect(lambda: self.csv())
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
        self.action_csv.setText(QCoreApplication.translate("MainWindow", u".csv", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_export_as.setTitle(QCoreApplication.translate("MainWindow", u"Export as ...", None))
    # retranslateUi

    def open(self):
        f_name, _ = QFileDialog.getOpenFileName(self.central_widget, 'Open file',
                                                filter="Abf files (*.abf);; Edh files(*.edh)")
        self.logics.open_abf(f_name)
        # print last abf read
        print(self.logics.abfs[len(self.logics.abfs)-1])
        print(len(self.logics.abfs))

    def csv(self):
        # TODO
        print("exporting csv... ")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())
