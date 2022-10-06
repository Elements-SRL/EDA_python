from PyQt5 import QtWidgets
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QRadioButton, QLabel, QLineEdit, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class FiltersWidget(QtWidgets.QWidget):

    def __init__(self):
        super(FiltersWidget, self).__init__()
        self.apply_filter_button = None
        self.preview_button = None
        self.cutoff_freq_line_edit = None
        self.cutoff_freq_label = None
        self.high_pass = None
        self.low_pass = None
        self.band_pass = None
        self.mpl_canvas = MplCanvas()

        self.setup()

    def setup(self):
        views_layout = QHBoxLayout()
        self.setWindowTitle("Filters")
        self.setMinimumSize(600, 500)
        self.setLayout(views_layout)
        first_col = QVBoxLayout()
        self.band_pass = QRadioButton("Band pass")
        self.low_pass = QRadioButton("Low pass")
        self.high_pass = QRadioButton("High pass")
        self.cutoff_freq_label = QLabel("Cutoff frequency")
        self.cutoff_freq_line_edit = QLineEdit()
        only_double = QDoubleValidator()
        only_double.setNotation(QDoubleValidator.StandardNotation)
        self.cutoff_freq_line_edit.setValidator(only_double)
        first_col.addWidget(self.band_pass)
        first_col.addWidget(self.low_pass)
        first_col.addWidget(self.high_pass)
        first_col.addWidget(self.cutoff_freq_label)
        first_col.addWidget(self.cutoff_freq_line_edit)
        first_col.addWidget(self.mpl_canvas)
        second_col = QVBoxLayout()
        views_layout.addLayout(first_col)
        views_layout.addLayout(second_col)
        buttons_line = QHBoxLayout()
        self.preview_button = QPushButton("Preview")
        # self.preview_button.pressed.connect(lambda : print("ciccia"))
        self.apply_filter_button = QPushButton("Apply filter")
        buttons_line.addWidget(self.preview_button)
        buttons_line.addWidget(self.apply_filter_button)
        first_col.addLayout(buttons_line)
        self.show()
