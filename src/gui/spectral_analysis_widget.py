import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numpy import ndarray
from scipy import signal


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class SpectralAnalysisWidget(QtWidgets.QWidget):

    def __init__(self, x: ndarray, y: ndarray):
        super(SpectralAnalysisWidget, self).__init__()
        views_layout = QVBoxLayout()
        self.setWindowTitle("Spectral Analysis")
        self.setMinimumSize(500, 600)
        self.setLayout(views_layout)
        self.mpl_canvas = MplCanvas()
        views_layout.addWidget(self.mpl_canvas)
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
