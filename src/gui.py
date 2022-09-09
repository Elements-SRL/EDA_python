import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QMenuBar, QStatusBar, QMenu, QAction, QFileDialog, QGridLayout, QFrame
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import logics

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.ax1 = None
        self.axs = None
        self.fig = None
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, sharex=True)
        super(MplCanvas, self).__init__(self.fig)


class UiMainWindow(object):
    logics = None

    def __init__(self):
        self.sc = None
        self.toolbar = None
        self.canvas = None
        self.figure = None
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

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        plot_layout = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(plot_layout, 0, 0, 0, 0)

        toolbar = NavigationToolbar(self.sc, main_window)
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.sc)

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

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", u"EDA", None))
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
                                                filter="Edh files(*.edh);;Abf files (*.abf)")
        self.logics.open(f_name)
        self.update_plot()

    def csv(self):
        # TODO
        print("exporting csv... ")

    def update_plot(self):
        abfs = self.logics.get_abfs()
        if len(abfs) <= 0:
            return
        self.sc.ax1.cla()
        self.sc.ax2.cla()
        i = 0
        for abf in abfs:
            # it's better not to display multiple channels and multiple sweeps in the same plot,
            # implementation could change in future
            if abf.sweepCount > 1:
                sweep_label = 0
                for sweep in range(abf.sweepCount):
                    multi_sweep_label = logics.get_channel_name(abf) + " sweep " + str(sweep_label)
                    self.sc.ax1.plot(abf.sweepX, abf.sweepY, label=multi_sweep_label)
                    sweep_label += 1
            else:
                label = logics.get_channel_name(abf)
                self.sc.ax1.plot(abf.sweepX, abf.sweepY, label=label)
                self.sc.ax2.plot(abf.sweepX, abf.sweepC, label=label)
            i += 1
        # set label with the last abf read
        self.sc.ax1.set_ylabel(abf.sweepLabelY)
        self.sc.ax2.set_xlabel(abf.sweepLabelX)
        self.sc.ax2.set_ylabel(abf.sweepLabelC)

        self.sc.ax1.legend()
        self.sc.ax2.legend()
        self.sc.draw()
