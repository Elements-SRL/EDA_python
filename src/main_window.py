from typing import List, Iterable

import matplotlib
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import logics
from src.gui.filters_widget import FiltersWidget
from src.gui.spectral_analysis_widget import SpectralAnalysisWidget
from src.metadata.data_classes.data_group import DataGroup

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        self.ax1 = None
        self.axs = None
        self.fig = None
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, sharex=True)
        super(MplCanvas, self).__init__(self.fig)


def show_empty_abfs_dialog(title, text, informative_text):
    # TODO show dialog to tell that file would be empty
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowTitle(title)
    message_box.setInformativeText(informative_text)
    message_box.exec()


class UiMainWindow(object):
    logics = None

    def __init__(self):
        self.spectral_analysis_widget: SpectralAnalysisWidget | None = None
        self.action_spectral_analysis = None
        self.model: QStandardItemModel | None = None
        self.tree_view: QTreeView | None = None
        self.outer_div: QHBoxLayout | None = None
        self.filter_widget: FiltersWidget | None = None
        self.action_open_filters = None
        self.menu_analyze = None
        self.action_open_visible_channels = None
        self.menu_view = None
        self.views_widget = None
        self.action_clear = None
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
        self.action_open_visible_channels = QAction(main_window)
        self.action_open_visible_channels.setObjectName(u"action_open_visible_channels")
        self.action_clear = QAction(main_window)
        self.action_clear.setObjectName(u"action_clear")
        self.action_open_filters = QAction(main_window)
        self.action_open_filters.setObjectName(u"action_open_filters")
        self.action_spectral_analysis = QAction(main_window)
        self.action_spectral_analysis.setObjectName(u"action_spectral_analysis")
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.outer_div = QHBoxLayout(self.central_widget)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(self.central_widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)

        self.sc = MplCanvas()

        plot_layout = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(plot_layout, 0, 0, 0, 0)
        toolbar = NavigationToolbar(self.sc, main_window)
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.sc)

        main_window.setCentralWidget(self.central_widget)
        # MENU BAR
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 722, 32))
        main_window.setMenuBar(self.menubar)
        # MENU FILE
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.actionOpen)
        # MENU EXPORT AS
        self.menu_export_as = QMenu(self.menu_file)
        self.menu_export_as.setObjectName(u"menu_export_as")
        self.menu_file.addAction(self.menu_export_as.menuAction())
        self.menu_export_as.addAction(self.action_csv)
        # Menu VIEW
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menubar.addAction(self.menu_view.menuAction())
        self.menu_view.addAction(self.action_open_visible_channels)
        self.menu_view.addAction(self.action_clear)
        # Menu ANALYZE
        self.menu_analyze = QMenu(self.menubar)
        self.menu_analyze.setObjectName(u"menu_analyze")
        self.menubar.addAction(self.menu_analyze.menuAction())
        self.menu_analyze.addAction(self.action_open_filters)
        self.menu_analyze.addAction(self.action_spectral_analysis)
        # STATUS BAR
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.status_bar)
        self.model = QStandardItemModel()
        # item3.clicked.connect(lambda: print("clicked"))
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setMaximumWidth(200)
        self.tree_view.doubleClicked.connect(self._select_data_group)
        self.gridLayout.addWidget(self.tree_view)
        self.outer_div.addWidget(self.tree_view)
        self.outer_div.addLayout(self.gridLayout)
        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.actionOpen.triggered.connect(lambda: self.open())
        self.action_csv.triggered.connect(lambda: self.csv())
        self.action_open_visible_channels.triggered.connect(lambda: self.open_views_window())
        self.action_clear.triggered.connect(lambda: self.clear())
        self.action_open_filters.triggered.connect(lambda: self.open_filters())
        self.action_spectral_analysis.triggered.connect(lambda: self._open_spectral_analysis())

    # setupUi

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", u"EDA", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        # if QT_CONFIG(status tip)
        self.actionOpen.setStatusTip(QCoreApplication.translate("MainWindow", u"Open an abf file", None))
        # endif // QT_CONFIG(status tip)
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        # endif // QT_CONFIG(shortcut)
        self.action_csv.setText(QCoreApplication.translate("MainWindow", u".csv", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menu_analyze.setTitle(QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.action_open_visible_channels.setText(
            QCoreApplication.translate("MainWindow", u"Visible channels/sweeps", None))
        self.action_clear.setText(QCoreApplication.translate("MainWindow", u"Clear current plots", None))
        self.menu_export_as.setTitle(QCoreApplication.translate("MainWindow", u"Export as ...", None))
        self.action_open_filters.setText(QCoreApplication.translate("MainWindow", u"Filters", None))
        self.action_spectral_analysis.setText(QCoreApplication.translate("MainWindow", u"Spectral analysis", None))

    # retranslateUi

    def open(self):
        f_name, _ = QFileDialog.getOpenFileName(None, 'Open file', filter="Edh files(*.edh);;Abf files (*.abf)")
        if f_name:
            self.logics.open(f_name)
            self._update_tree_view()
            self._update_plot()

    def csv(self):
        # if list is empty
        if self.logics.metadata.is_empty():
            show_empty_abfs_dialog("Nothing to export.", "Export csv", "Open a file and try again.")
            return
        # TODO hint or choose a default name?
        path_to_file, _ = QFileDialog.getSaveFileName(None, 'Save as', filter="Csv files(*.csv)")
        if not str(path_to_file).endswith(".csv"):
            path_to_file = path_to_file + ".csv"

        # TODO show progress_bar (?)
        self.logics.export(path_to_file)

    def _update_plot(self):
        self.sc.ax1.cla()
        self.sc.ax2.cla()
        # self.sc.ax1.set_title("Channel 0")
        # self.sc.ax2.set_title("Channel 1")
        if self.logics.is_all_data_hidden():
            # clear plot
            self.sc.draw()
            return
        x = self.logics.metadata.get_x()
        data = self.logics.metadata.get_visible_data()
        for d in data:
            if d.ch == 0:
                self.sc.ax1.plot(x, d.y, label=d.name)
            elif d.ch == 1:
                self.sc.ax2.plot(x, d.y, label=d.name)
        self.sc.ax1.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_y)
        self.sc.ax2.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_c)
        self.sc.ax2.set_xlabel(self.logics.metadata.selected_data_group.sweep_label_x)
        self.sc.ax1.legend(loc='upper right')
        self.sc.ax2.legend(loc='upper right')
        self.sc.draw()

    def clear(self):
        # TODO FIRST ASK FOR CONFIRMATION
        self.logics.clear()
        self.sc.ax1.cla()
        self.sc.ax2.cla()
        self.sc.draw()

    def open_views_window(self):
        if self.logics.is_all_data_hidden():
            show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
            return
        views_layout = QVBoxLayout()
        self.views_widget = QWidget()
        self.views_widget.setWindowTitle("Views")
        self.views_widget.setMinimumSize(200, 300)
        self.views_widget.setLayout(views_layout)
        buttons = []
        views_layout.deleteLater()
        for d in self.logics.metadata.selected_data_group.basic_data:
            b = QCheckBox(d.name)
            views_layout.addWidget(b)
            b.setChecked(d.visible)
            buttons.append(b)
        apply_button = QPushButton("Show selected channels")
        apply_button.clicked.connect(lambda: self.hide_sweeps(buttons))
        views_layout.addWidget(apply_button)
        self.views_widget.show()

    def hide_sweeps(self, buttons: List[QCheckBox]):
        for b in buttons:
            self.logics.metadata.set_visibility(b.text(), b.isChecked())
        self._update_plot()

    def open_filters(self):
        if self.logics.is_all_data_hidden():
            show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
            return
        if self.filter_widget is None:
            self.filter_widget = FiltersWidget(self.logics.metadata.selected_data_group.sampling_rate)
            self.filter_widget.preview_button.pressed.connect(lambda: self._filter_preview())
            self.filter_widget.apply_filter_button.pressed.connect(lambda: self._apply_filter())
            self._filter_preview()
        else:
            self.filter_widget.show()

    def _open_spectral_analysis(self):
        # if self.logics.is_all_data_hidden():
        #     show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
        #     return
        if self.spectral_analysis_widget is None:
            self.spectral_analysis_widget = SpectralAnalysisWidget(np.array([1, 2, 3]), np.array([1, 2, 3]), "ciccia",
                                                                   "culo")
        else:
            self.spectral_analysis_widget.draw(np.array([3, 2, 1]), np.array([1, 2, 3]), "ciccia", "culo")
            self.spectral_analysis_widget.show()

    def _filter_preview(self):
        filter_arguments = self.filter_widget.get_filter_args()
        b, a = self.logics.filter_preview(filter_arguments)
        self.filter_widget.draw_preview(b, a)

    def _apply_filter(self):
        filter_arguments = self.filter_widget.get_filter_args()
        self.logics.filter_selected_data_group(filter_arguments)
        self.filter_widget.close()
        self._update_plot()
        self._update_tree_view()

    def _select_data_group(self, index: QModelIndex):
        self.logics.select_data_group(index.data())
        self._update_plot()

    def _update_tree_view(self):
        self.model.clear()
        items = _recursive_bundle(self.logics.metadata.data_groups)
        for i in items:
            self.model.appendRow(i)


def _recursive_bundle(data_groups: Iterable[DataGroup]) -> List[QStandardItem]:
    items = []
    for dg in data_groups:
        if len(dg.data_groups) == 0:
            item = QStandardItem(dg.name)
            item.setEditable(False)
            items.append(item)
        elif len(dg.data_groups) > 0:
            dgs = dg.data_groups
            item = QStandardItem(dg.name)
            item.setEditable(False)
            internal_items = _recursive_bundle(dgs)
            for i in internal_items:
                item.appendRow(i)
            items.append(item)
    return items
