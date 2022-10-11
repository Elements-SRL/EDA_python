from typing import Tuple, List

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from numpy import ndarray
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class SpectralAnalysisWidget(QtWidgets.QWidget):

    def __init__(self, spectra: List[Tuple[ndarray, ndarray]], y_label: str):
        super(SpectralAnalysisWidget, self).__init__()
        views_layout = QHBoxLayout()
        first_col = QVBoxLayout()
        second_col = QVBoxLayout()
        self.setWindowTitle("Spectral Analysis")
        self.setMinimumSize(500, 600)
        self.setLayout(views_layout)
        self.mpl_canvas = MplCanvas()
        first_col.addWidget(QLabel("Channel"))
        self.rb_ch0 = QRadioButton("0")
        first_col.addWidget(self.rb_ch0)
        self.rb_ch1 = QRadioButton("1")
        first_col.addWidget(self.rb_ch1)
        views_layout.addLayout(first_col)
        views_layout.addLayout(second_col)
        views_layout.addWidget(self.mpl_canvas)
        self.draw(spectra, y_label)
        self.show()

    def draw(self, spectra: List[Tuple[ndarray, ndarray]], y_label: str):
        self.mpl_canvas.axes.cla()
        self.mpl_canvas.axes.set_title('Power Spectral Density')
        self.mpl_canvas.axes.set_xlabel("Frequency [Hz]")
        self.mpl_canvas.axes.set_ylabel(y_label)
        for s in spectra:
            f, Pxx_den = s
            self.mpl_canvas.axes.plot(f, Pxx_den)
        self.mpl_canvas.axes.yaxis.grid()
        self.mpl_canvas.axes.xaxis.grid()
        self.mpl_canvas.draw()
