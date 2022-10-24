from typing import List, Iterable
import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RangeSlider
from logics import Logics
from src.gui import views_widget
from src.gui.filters_widget import FiltersWidget
from src.gui.mpl_canvas import MplCanvas
from src.metadata.data_classes.data_group import DataGroup
import src.gui.dialogs as dialogs

matplotlib.use("Qt5Agg")


class UiMainWindow(object):
    def __init__(self):
        self.action_boltzmann_fitting: QAction | None = None
        self.action_gaussian_fitting: QAction | None = None
        self.action_power_law_fitting: QAction | None = None
        self.action_exponential_fitting: QAction | None = None
        self.action_quadratic_fit: QAction | None = None
        self.action_linear_fit: QAction | None = None
        self.menu_fit = None
        self.action_create_range = None
        self.menu_roi = None
        self.lower_limit: List[Line2D] | None = []
        self.upper_limit: List[Line2D] | None = []
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
        self.logics = Logics()

    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName("MainWindow")
        main_window.resize(800, 600)
        self.actionOpen = QAction(main_window)
        self.actionOpen.setObjectName("actionOpen")
        self.action_csv = QAction(main_window)
        self.action_csv.setObjectName("action_csv")
        self.action_open_visible_channels = QAction(main_window)
        self.action_open_visible_channels.setObjectName("action_open_visible_channels")
        self.action_clear = QAction(main_window)
        self.action_clear.setObjectName("action_clear")
        self.action_open_filters = QAction(main_window)
        self.action_open_filters.setObjectName("action_open_filters")
        self.action_spectral_analysis = QAction(main_window)
        self.action_spectral_analysis.setObjectName("action_spectral_analysis")
        self.action_histogram = QAction(main_window)
        self.action_histogram.setObjectName("action_histogram")
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.outer_div = QHBoxLayout(self.central_widget)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QFrame(self.central_widget)
        self.frame_2.setObjectName("frame_2")
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
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 722, 32))
        main_window.setMenuBar(self.menubar)
        # MENU FILE
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_file.addAction(self.actionOpen)
        # MENU EXPORT AS
        self.menu_export_as = QMenu(self.menu_file)
        self.menu_export_as.setObjectName("menu_export_as")
        self.menu_file.addAction(self.menu_export_as.menuAction())
        self.menu_export_as.addAction(self.action_csv)
        # Menu VIEW
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName("menu_view")
        self.menubar.addAction(self.menu_view.menuAction())
        self.menu_view.addAction(self.action_open_visible_channels)
        self.menu_view.addAction(self.action_clear)
        # Menu ANALYZE
        self.menu_analyze = QMenu(self.menubar)
        self.menu_analyze.setObjectName("menu_analyze")
        self.menubar.addAction(self.menu_analyze.menuAction())
        self.menu_analyze.addAction(self.action_open_filters)
        self.menu_analyze.addAction(self.action_spectral_analysis)
        self.menu_analyze.addAction(self.action_histogram)
        # Menu FIT
        self.menu_fit = QMenu(self.menu_analyze)
        self.menu_fit.setObjectName("menu_fit")
        self.menu_analyze.addAction(self.menu_fit.menuAction())
        # Actions for MENU FIT
        self.action_linear_fit = QAction(main_window)
        self.action_linear_fit.setObjectName("action_linear_fit")
        self.action_quadratic_fit = QAction(main_window)
        self.action_quadratic_fit.setObjectName("action_quadratic_fit")
        self.action_exponential_fitting = QAction(main_window)
        self.action_exponential_fitting.setObjectName("action_exponential_fitting")
        self.action_power_law_fitting = QAction(main_window)
        self.action_power_law_fitting.setObjectName("action_power_law_fitting")
        self.action_gaussian_fitting = QAction(main_window)
        self.action_gaussian_fitting.setObjectName("action_gaussian_fitting")
        self.action_boltzmann_fitting = QAction(main_window)
        self.action_boltzmann_fitting.setObjectName("action_boltzmann_fitting")
        # Add actions to menu fit
        self.menu_fit.addAction(self.action_linear_fit)
        self.menu_fit.addAction(self.action_quadratic_fit)
        self.menu_fit.addAction(self.action_exponential_fitting)
        self.menu_fit.addAction(self.action_power_law_fitting)
        self.menu_fit.addAction(self.action_gaussian_fitting)
        self.menu_fit.addAction(self.action_boltzmann_fitting)
        # Menu ROI
        self.menu_roi = QMenu(self.menubar)
        self.menu_roi.setObjectName("menu_roi")
        self.menubar.addAction(self.menu_roi.menuAction())
        self.action_create_range = QAction(main_window)
        self.action_create_range.setObjectName("action_create_range")
        self.menu_roi.addAction(self.action_create_range)
        # STATUS BAR
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName("statusbar")
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
        self.action_open_visible_channels.triggered.connect(
            lambda: self.open_views_window()
        )
        self.action_clear.triggered.connect(lambda: self.clear())
        self.action_open_filters.triggered.connect(lambda: self.open_filters())
        self.action_spectral_analysis.triggered.connect(
            lambda: self._open_spectral_analysis()
        )
        self.action_histogram.triggered.connect(lambda: self._perform_histogram())
        self.action_create_range.triggered.connect(
            lambda: self._create_range()
        )
        self.action_gaussian_fitting.triggered.connect(lambda: self._perform_fit('gaussian'))
        self.action_power_law_fitting.triggered.connect(lambda: self._perform_fit('power_law'))
        self.action_exponential_fitting.triggered.connect(lambda: self._perform_fit('exponential'))
        self.action_quadratic_fit.triggered.connect(lambda: self._perform_fit('quadratic'))
        self.action_linear_fit.triggered.connect(lambda: self._perform_fit('linear'))
        self.action_boltzmann_fitting.triggered.connect(lambda: self._perform_fit('boltzmann'))

    # setupUi

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(
            QCoreApplication.translate("MainWindow", "EDA", None)
        )
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", "Open", None))
        # if QT_CONFIG(status tip)
        self.actionOpen.setStatusTip(
            QCoreApplication.translate("MainWindow", "Open an abf file", None)
        )
        # endif // QT_CONFIG(status tip)
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_csv.setText(QCoreApplication.translate("MainWindow", ".csv", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menu_view.setTitle(QCoreApplication.translate("MainWindow", "View", None))
        self.menu_analyze.setTitle(
            QCoreApplication.translate("MainWindow", "Analyze", None)
        )
        self.menu_fit.setTitle(
            QCoreApplication.translate("MainWindow", "Fit", None)
        )
        self.menu_roi.setTitle(
            QCoreApplication.translate("MainWindow", "Region of interest", None)
        )
        self.action_open_visible_channels.setText(
            QCoreApplication.translate("MainWindow", "Visible channels/sweeps", None)
        )
        self.action_clear.setText(
            QCoreApplication.translate("MainWindow", "Clear current plots", None)
        )
        self.menu_export_as.setTitle(
            QCoreApplication.translate("MainWindow", "Export as ...", None)
        )
        self.action_open_filters.setText(
            QCoreApplication.translate("MainWindow", "Filters", None)
        )
        self.action_spectral_analysis.setText(
            QCoreApplication.translate("MainWindow", "Spectral analysis", None)
        )
        self.action_histogram.setText(
            QCoreApplication.translate("MainWindow", "Histogram", None)
        )
        self.action_create_range.setText(
            QCoreApplication.translate("MainWindow", "Create ROI", None)
        )
        self.action_gaussian_fitting.setText(
            QCoreApplication.translate("MainWindow", "Gaussian", None)
        )
        self.action_power_law_fitting.setText(
            QCoreApplication.translate("MainWindow", "Power Law", None)
        )
        self.action_exponential_fitting.setText(
            QCoreApplication.translate("MainWindow", "Exponential", None)
        )
        self.action_quadratic_fit.setText(
            QCoreApplication.translate("MainWindow", "Quadratic", None)
        )
        self.action_linear_fit.setText(
            QCoreApplication.translate("MainWindow", "Linear", None)
        )
        self.action_boltzmann_fitting.setText(
            QCoreApplication.translate("MainWindow", "Boltzmann", None)
        )

    # retranslateUi

    def open(self):
        f_name, _ = QFileDialog.getOpenFileName(
            None, "Open file", filter="Edh files(*.edh);;Abf files (*.abf)"
        )
        if f_name:
            self.logics.open(f_name)
            self._update_tree_view()
            self._update_plot()

    def csv(self):
        # if list is empty
        if self.logics.metadata.is_empty():
            dialogs.show_empty_abfs_dialog(
                "Nothing to export.", "Export csv", "Open a file and try again."
            )
            return
        # TODO hint or choose a default name?
        path_to_file, _ = QFileDialog.getSaveFileName(
            None, "Save as", filter="Csv files(*.csv)"
        )
        if not str(path_to_file).endswith(".csv"):
            path_to_file = path_to_file + ".csv"

        # TODO show progress_bar (?)
        self.logics.export(path_to_file)

    def _update_plot(self):
        self.mpl.ax1.cla()
        self.mpl.ax2.cla()
        self.mpl.only_one_ax.cla()
        self.mpl.fig.tight_layout()
        self.mpl.clean_slider()
        self.mpl.fig.subplots_adjust(bottom=0.15)
        if self.logics.is_all_data_hidden():
            # clear plot
            self.mpl.draw()
            return
        data = self.logics.metadata.get_visible_data()
        axis_number = len(
            {bd.axis for bd in self.logics.metadata.selected_data_group.basic_data}
        )
        is_histogram = self.logics.metadata.selected_data_group.type.startswith("hist")
        x = self.logics.metadata.get_x()
        self.mpl.slider = RangeSlider(
            self.mpl.slider_ax, "Range selector", x.min(), x.max()
        )
        if is_histogram:
            self.mpl.set_one_plot()
            w = x[1] - x[0]
            for d in data:
                self.mpl.only_one_ax.bar(x, d.y, label=d.name, width=w)
            self.mpl.only_one_ax.set_ylabel(
                self.logics.metadata.selected_data_group.sweep_label_y
            )
            self.mpl.only_one_ax.set_xlabel(
                self.logics.metadata.selected_data_group.sweep_label_x
            )
            self.mpl.only_one_ax.legend(loc="upper right")
        elif axis_number == 1:
            self.mpl.set_one_plot()
            for d in data:
                self.mpl.only_one_ax.plot(x, d.y, label=d.name)
            self.mpl.only_one_ax.set_ylabel(
                self.logics.metadata.selected_data_group.sweep_label_y
            )
            self.mpl.only_one_ax.set_xlabel(
                self.logics.metadata.selected_data_group.sweep_label_x
            )
            self.mpl.only_one_ax.legend(loc="upper right")
        else:
            self.mpl.set_two_plots()
            for d in data:
                if d.axis == 0:
                    self.mpl.ax1.plot(x, d.y, label=d.name, linewidth=1)
                elif d.axis == 1:
                    self.mpl.ax2.plot(x, d.y, label=d.name)
                self.mpl.ax1.set_ylabel(
                    self.logics.metadata.selected_data_group.sweep_label_y
                )
                self.mpl.ax1.set_xlabel(
                    self.logics.metadata.selected_data_group.sweep_label_x
                )
                self.mpl.ax2.set_ylabel(
                    self.logics.metadata.selected_data_group.sweep_label_c
                )
                self.mpl.ax2.set_xlabel(
                    self.logics.metadata.selected_data_group.sweep_label_x
                )
                self.mpl.ax1.legend(loc="upper right")
                self.mpl.ax2.legend(loc="upper right")
        self.mpl.set_func(self._update_limit_lines)
        self._init_limit_lines(self.mpl.slider.val, self.mpl.get_active_axis())
        self.mpl.draw()

    def clear(self):
        # TODO FIRST ASK FOR CONFIRMATION
        self.logics.clear()
        self.mpl.ax1.cla()
        self.mpl.ax2.cla()
        self.mpl.draw()

    def open_views_window(self):
        if self._manage_empty_metadata():
            return
        self.views_widget = views_widget.show_views_widget(self.logics.metadata.selected_data_group.basic_data,
                                                           self._hide_sweeps)

    def _hide_sweeps(self, checkboxes: List[QCheckBox]):
        for cb in checkboxes:
            self.logics.metadata.set_visibility(cb.text(), cb.isChecked())
        self._update_plot()
        self.views_widget.close()

    def open_filters(self):
        if self._manage_empty_metadata():
            return
        if self.filter_widget is None:
            self.filter_widget = FiltersWidget(
                self.logics.metadata.selected_data_group.sampling_rate
            )
            self.filter_widget.preview_button.pressed.connect(
                lambda: self._filter_preview()
            )
            self.filter_widget.apply_filter_button.pressed.connect(
                lambda: self._apply_filter()
            )
            self._filter_preview()
        else:
            self.filter_widget.show()

    def _open_spectral_analysis(self):
        if self._manage_empty_metadata():
            return
        self.logics.spectral_analysis()
        self._update_plot()
        self._update_tree_view()

    def _perform_histogram(self):
        if self._manage_empty_metadata():
            return
        self.logics.hist()
        self._update_plot()
        self._update_tree_view()

    def _filter_preview(self):
        filter_arguments = self.filter_widget.get_filter_args()
        if (filter_arguments.b_type == "bandpass" and
                filter_arguments.cutoff_frequency > filter_arguments.other_cutoff_frequency):
            dialogs.show_warning("Incorrect frequencies",
                                 "Bandpass filters require two cutoff frequencies",
                                 "Incorrect filter: the second cutoff frequency is lower than the first one")
            return
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

    def _init_limit_lines(self, val, axs: Iterable[Axes]):
        self.upper_limit.clear()
        self.lower_limit.clear()
        for ax in axs:
            self.lower_limit.append(ax.axvline(val[0], color="k"))
            self.upper_limit.append(ax.axvline(val[1], color="k"))
        self.mpl.fig.canvas.draw_idle()

    def _update_limit_lines(self, val):
        for ll in self.lower_limit:
            ll.set_xdata(val[0])
        for ul in self.upper_limit:
            ul.set_xdata(val[1])
        self.mpl.fig.canvas.draw_idle()

    def _create_range(self):
        if self._manage_empty_metadata():
            return
        x_min, x_max = self.mpl.slider.val
        self.logics.create_new_range(x_min, x_max)
        self._update_plot()
        self._update_tree_view()

    def _perform_fit(self, func_name: str):
        if self._manage_empty_metadata():
            return
        self.logics.fit(func_name)
        self._update_plot()
        self._update_tree_view()

    def _manage_empty_metadata(self) -> bool:
        if self.logics.metadata.is_empty():
            dialogs.show_empty_abfs_dialog(
                "Empty window", "Nothing to display", "No data has been opened."
            )
            return True
        return False


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
