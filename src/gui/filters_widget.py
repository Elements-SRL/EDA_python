import numpy as np
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import ndarray
from scipy import signal

from src.analysis.filters.filter_arguments import FilterArguments


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class FiltersWidget(QWidget):

    def __init__(self, fs: float):
        super(FiltersWidget, self).__init__()
        self.fs = fs
        views_layout = QVBoxLayout()
        self.setWindowTitle("Filters")
        self.setMinimumSize(500, 600)
        self.setLayout(views_layout)
        content_column = QHBoxLayout()
        first_internal_col = QVBoxLayout()
        # FS Label
        fs_label = QLabel("Frequency: " + str(fs))
        first_internal_col.addWidget(fs_label)
        # RadioButtons
        self.band_pass_radio_button = QRadioButton("Band pass")
        self.low_pass_radio_button = QRadioButton("Low pass")
        self.high_pass_radio_button = QRadioButton("High pass")
        # Type Combobox
        self.type_label = QLabel("Type")
        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["butter", "bessel", "cheby1"])
        # Order SpinBox
        self.order_label = QLabel("Order")
        self.order_spin_box = QSpinBox()
        self.order_spin_box.setValue(4)
        # Cutoff Spinbox
        self.cutoff_freq_label = QLabel("Cutoff frequency (Hz) - Max value is: " + str(fs / 2 - 1))
        self.cutoff_freq_spin_box = QDoubleSpinBox()
        self.cutoff_freq_spin_box.setMinimum(1)
        self.cutoff_freq_spin_box.setMaximum(fs / 2 - 1)
        self.cutoff_freq_spin_box.setEnabled(False)
        # Other cutoff Spinbox
        self.other_cutoff_freq_label = QLabel("Cutoff frequency (Hz) - Max value is: " + str(fs / 2 - 1))
        self.other_cutoff_freq_spin_box = QDoubleSpinBox()
        self.other_cutoff_freq_spin_box.setMinimum(1)
        self.other_cutoff_freq_spin_box.setMaximum(fs / 2 - 1)
        self.other_cutoff_freq_spin_box.setEnabled(False)
        first_internal_col.addWidget(self.band_pass_radio_button)
        first_internal_col.addWidget(self.low_pass_radio_button)
        first_internal_col.addWidget(self.high_pass_radio_button)
        first_internal_col.addWidget(self.type_label)
        first_internal_col.addWidget(self.type_combo_box)
        first_internal_col.addWidget(self.order_label)
        first_internal_col.addWidget(self.order_spin_box)
        first_internal_col.addWidget(self.cutoff_freq_label)
        first_internal_col.addWidget(self.cutoff_freq_spin_box)
        first_internal_col.addWidget(self.other_cutoff_freq_label)
        first_internal_col.addWidget(self.other_cutoff_freq_spin_box)
        second_internal_col = QVBoxLayout()
        self.mpl_canvas = MplCanvas()
        second_internal_col.addWidget(self.mpl_canvas)
        content_column.addLayout(first_internal_col)
        content_column.addLayout(second_internal_col)
        views_layout.addLayout(content_column)
        # Push buttons
        buttons_line = QHBoxLayout()
        self.preview_button = QPushButton("Preview")
        self.apply_filter_button = QPushButton("Apply filter")
        self.preview_button.setEnabled(False)
        self.apply_filter_button.setEnabled(False)
        buttons_line.addWidget(self.preview_button)
        buttons_line.addWidget(self.apply_filter_button)
        views_layout.addLayout(buttons_line)
        self.band_pass_radio_button.pressed.connect(lambda: self._activate_band_pass())
        self.high_pass_radio_button.pressed.connect(lambda: self._deactivate_band_pass())
        self.low_pass_radio_button.pressed.connect(lambda: self._deactivate_band_pass())
        self.low_pass_radio_button.setChecked(True)
        self._deactivate_band_pass()
        self.show()

    def draw_preview(self, b: ndarray, a: ndarray):
        self.mpl_canvas.axes.cla()
        w, h = signal.freqz(b, a, fs=self.fs)
        self.mpl_canvas.axes.set_title('Filter frequency response')
        self.mpl_canvas.axes.set_xlabel('Frequency [Hz]')
        self.mpl_canvas.axes.set_ylabel('Amplitude [db]')
        self.mpl_canvas.axes.semilogx(w, 20 * np.log10(np.abs(h)))
        self.mpl_canvas.axes.yaxis.grid()
        self.mpl_canvas.axes.xaxis.grid()
        self.mpl_canvas.draw()

    def _activate_band_pass(self):
        self.cutoff_freq_spin_box.setEnabled(True)
        self.other_cutoff_freq_spin_box.setEnabled(True)
        self.preview_button.setEnabled(True)
        self.apply_filter_button.setEnabled(True)

    def _deactivate_band_pass(self):
        self.cutoff_freq_spin_box.setEnabled(True)
        self.other_cutoff_freq_spin_box.setEnabled(False)
        self.preview_button.setEnabled(True)
        self.apply_filter_button.setEnabled(True)

    def get_b_type(self) -> str:
        if self.low_pass_radio_button.isChecked():
            return "lowpass"
        if self.band_pass_radio_button.isChecked():
            return "bandpass"
        if self.high_pass_radio_button.isChecked():
            return "highpass"

    def get_filter_args(self) -> FilterArguments:
        f_type = self.type_combo_box.currentText()
        order = self.order_spin_box.value()
        cutoff_frequency = self.cutoff_freq_spin_box.value()
        other_cutoff_frequency = self.other_cutoff_freq_spin_box.value()
        b_type = self.get_b_type()
        return FilterArguments(filter_type=f_type, b_type=b_type, cutoff_frequency=cutoff_frequency, order=order,
                               other_cutoff_frequency=other_cutoff_frequency, fs=self.fs)
