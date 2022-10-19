from typing import List, Iterable

import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

import logics
from src.gui.filters_widget import FiltersWidget
from src.metadata.data_classes.data_group import DataGroup

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        self.fig = plt.figure()
        self.ax1 = plt.subplot(211)
        self.ax2 = plt.subplot(212, sharex=self.ax1)
        self.only_one_ax = plt.subplot(111)
        super(MplCanvas, self).__init__(self.fig)

    def set_one_plot(self):
        if self.only_one_ax not in self.fig.axes:
            self.fig.delaxes(self.ax1)
            self.fig.delaxes(self.ax2)
            self.only_one_ax = plt.subplot(111)

    def set_two_plots(self):
        if self.only_one_ax in self.fig.axes:
            self.fig.delaxes(self.only_one_ax)
            self.ax1 = plt.subplot(211)
            self.ax2 = plt.subplot(212, sharex=self.ax1)


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
        self.action_histogram = None
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
        self.mpl: MplCanvas | None = None
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
        self.action_histogram = QAction(main_window)
        self.action_histogram.setObjectName(u"action_histogram")
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

        self.mpl = MplCanvas()
        self.mpl.set_two_plots()
        plot_layout = QtWidgets.QVBoxLayout()
        self.gridLayout.addLayout(plot_layout, 0, 0, 0, 0)
        toolbar = NavigationToolbar(self.mpl, main_window)
        plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.mpl)

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
        self.menu_analyze.addAction(self.action_histogram)
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
        self.action_histogram.triggered.connect(lambda: self._perform_histogram())

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
        self.action_histogram.setText(QCoreApplication.translate("MainWindow", u"Histogram", None))

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
        self.mpl.ax1.cla()
        self.mpl.ax2.cla()
        self.mpl.only_one_ax.cla()
        # self.mpl.ax1.set_title("Channel 0")
        # self.mpl.ax2.set_title("Channel 1")
        if self.logics.is_all_data_hidden():
            # clear plot
            self.mpl.draw()
            return
        data = self.logics.metadata.get_visible_data()
        axis_number = len({bd.axis for bd in self.logics.metadata.selected_data_group.basic_data})
        is_histogram = self.logics.metadata.selected_data_group.type.startswith("hist")
        x = self.logics.metadata.get_x()
        if is_histogram:
            self.mpl.set_one_plot()
            for d in data:
                w = x[1] - x[0]
                self.mpl.only_one_ax.bar(x, d.y, label=d.name, width=w)
            self.mpl.only_one_ax.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_y)
            self.mpl.only_one_ax.set_xlabel(self.logics.metadata.selected_data_group.sweep_label_x)
            self.mpl.only_one_ax.legend(loc='upper right')
        elif axis_number == 1:
            self.mpl.set_one_plot()
            for d in data:
                self.mpl.only_one_ax.plot(x, d.y, label=d.name)
            self.mpl.only_one_ax.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_y)
            self.mpl.only_one_ax.set_xlabel(self.logics.metadata.selected_data_group.sweep_label_x)
            self.mpl.only_one_ax.legend(loc='upper right')
        else:
            self.mpl.set_two_plots()
            for d in data:
                if d.axis == 0:
                    self.mpl.ax1.plot(x, d.y, label=d.name, linewidth=1)
                elif d.axis == 1:
                    self.mpl.ax2.plot(x, d.y, label=d.name)
                self.mpl.ax1.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_y)
                self.mpl.ax1.set_xlabel(self.logics.metadata.selected_data_group.sweep_label_x)
                self.mpl.ax2.set_ylabel(self.logics.metadata.selected_data_group.sweep_label_c)
                self.mpl.ax2.set_xlabel(self.logics.metadata.selected_data_group.sweep_label_x)
                self.mpl.ax1.legend(loc='upper right')
                self.mpl.ax2.legend(loc='upper right')
        self.mpl.draw()

    def clear(self):
        # TODO FIRST ASK FOR CONFIRMATION
        self.logics.clear()
        self.mpl.ax1.cla()
        self.mpl.ax2.cla()
        self.mpl.draw()

    def open_views_window(self):
        if self.logics.is_all_data_hidden():
            show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
            return
        views_layout = QVBoxLayout()
        scroll_layout = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.views_widget = QWidget()
        self.views_widget.setWindowTitle("Views")
        self.views_widget.setMinimumSize(200, 300)
        self.views_widget.setLayout(views_layout)
        buttons = []
        views_layout.deleteLater()
        for d in self.logics.metadata.selected_data_group.basic_data:
            b = QCheckBox(d.name)
            scroll_layout.addWidget(b)
            b.setChecked(d.visible)
            buttons.append(b)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        views_layout.addWidget(scroll_area)
        apply_button = QPushButton("Show selected channels")
        apply_button.clicked.connect(lambda: self.hide_sweeps(buttons))
        views_layout.addWidget(apply_button)
        self.views_widget.show()

    def hide_sweeps(self, buttons: List[QCheckBox]):
        for b in buttons:
            self.logics.metadata.set_visibility(b.text(), b.isChecked())
        self._update_plot()
        self.views_widget.close()

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
        if self.logics.is_all_data_hidden():
            show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
            return
        self.logics.spectral_analysis()
        self._update_plot()
        self._update_tree_view()

    def _perform_histogram(self):
        if self.logics.is_all_data_hidden():
            show_empty_abfs_dialog("Empty window", "Nothing to display", "No data has been opened.")
            return
        self.logics.hist()
        self._update_plot()
        self._update_tree_view()

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
