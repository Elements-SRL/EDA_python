from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from scipy import signal


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class FiltersWidget(QtWidgets.QWidget):

    def __init__(self):
        super(FiltersWidget, self).__init__()
        views_layout = QHBoxLayout()
        self.setWindowTitle("Filters")
        self.setMinimumSize(600, 500)
        self.setLayout(views_layout)
        first_col = QVBoxLayout()
        # RadioButtons
        self.band_pass_radio_button = QRadioButton("Band pass")
        self.low_pass_radio_button = QRadioButton("Low pass")
        self.high_pass_radio_button = QRadioButton("High pass")
        # Type Combobox
        self.type_label = QLabel("Type")
        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(["butter"])
        # Order SpinBox
        self.order_label = QLabel("Order")
        self.order_spin_box = QSpinBox()
        self.order_spin_box.setValue(4)
        # Cutoff Spinbox
        self.cutoff_freq_label = QLabel("Cutoff frequency (Hz)")
        self.cutoff_freq_spin_box = QDoubleSpinBox()
        # TODO is it enough?
        self.cutoff_freq_spin_box.setMaximum(5000.000)
        self.cutoff_freq_spin_box.setValue(100.00)
        self.cutoff_freq_spin_box.setEnabled(False)
        # Other cutoff Spinbox
        self.other_cutoff_freq_label = QLabel("Cutoff frequency (Hz)")
        self.other_cutoff_freq_spin_box = QDoubleSpinBox()
        # TODO is it enough?
        self.other_cutoff_freq_spin_box.setMaximum(5000.000)
        self.other_cutoff_freq_spin_box.setValue(300.00)
        self.other_cutoff_freq_spin_box.setEnabled(False)
        first_col.addWidget(self.band_pass_radio_button)
        first_col.addWidget(self.low_pass_radio_button)
        first_col.addWidget(self.high_pass_radio_button)
        first_col.addWidget(self.type_label)
        first_col.addWidget(self.type_combo_box)
        first_col.addWidget(self.order_label)
        first_col.addWidget(self.order_spin_box)
        first_col.addWidget(self.cutoff_freq_label)
        first_col.addWidget(self.cutoff_freq_spin_box)
        first_col.addWidget(self.other_cutoff_freq_label)
        first_col.addWidget(self.other_cutoff_freq_spin_box)
        self.mpl_canvas = MplCanvas()
        first_col.addWidget(self.mpl_canvas)
        second_col = QVBoxLayout()
        views_layout.addLayout(first_col)
        views_layout.addLayout(second_col)
        # Push buttons
        buttons_line = QHBoxLayout()
        self.preview_button = QPushButton("Preview")
        self.apply_filter_button = QPushButton("Apply filter")
        buttons_line.addWidget(self.preview_button)
        buttons_line.addWidget(self.apply_filter_button)
        first_col.addLayout(buttons_line)
        self.preview_button.pressed.connect(lambda: self.preview_action())
        self.band_pass_radio_button.pressed.connect(lambda: self._activate_band_pass())
        self.high_pass_radio_button.pressed.connect(lambda: self._deactivate_band_pass())
        self.low_pass_radio_button.pressed.connect(lambda: self._deactivate_band_pass())
        self.show()

    def preview_action(self):
        self.mpl_canvas.axes.cla()
        order = self.order_spin_box.value()
        cutoff_frequency = self.cutoff_freq_spin_box.value()
        if self.low_pass_radio_button.isChecked():
            filter_type = "lowpass"
        if self.band_pass_radio_button.isChecked():
            filter_type = "bandpass"
        if self.high_pass_radio_button.isChecked():
            filter_type = "highpass"
        if self.band_pass_radio_button.isChecked():
            other_cutoff_frequency = self.other_cutoff_freq_spin_box.value()
            b, a = signal.butter(order, [cutoff_frequency, other_cutoff_frequency], filter_type, analog=True)
        else:
            b, a = signal.butter(order, cutoff_frequency, filter_type, analog=True)
        w, h = signal.freqs(b, a)
        self.mpl_canvas.axes.set_title('Butterworth filter frequency response')
        self.mpl_canvas.axes.set_xlabel('Frequency [radians / second]')
        self.mpl_canvas.axes.set_ylabel('Amplitude [dB]')
        self.mpl_canvas.axes.plot(w, h)
        self.mpl_canvas.draw()

    def _activate_band_pass(self):
        self.cutoff_freq_spin_box.setEnabled(True)
        self.other_cutoff_freq_spin_box.setEnabled(True)

    def _deactivate_band_pass(self):
        self.cutoff_freq_spin_box.setEnabled(True)
        self.other_cutoff_freq_spin_box.setEnabled(False)
