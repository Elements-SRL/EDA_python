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

    def __init__(self, x: ndarray, y: ndarray, x_label: str, y_label: str):
        super(SpectralAnalysisWidget, self).__init__()
        views_layout = QVBoxLayout()
        self.setWindowTitle("Spectral Analysis")
        self.setMinimumSize(500, 600)
        self.setLayout(views_layout)
        self.mpl_canvas = MplCanvas()
        views_layout.addWidget(self.mpl_canvas)
        self.draw(x, y, x_label, y_label)
        self.show()

    def draw(self, x: ndarray, y: ndarray, x_label: str, y_label: str):
        self.mpl_canvas.axes.cla()
        self.mpl_canvas.axes.set_title('Spectral Analysis')
        self.mpl_canvas.axes.set_xlabel(x_label)
        self.mpl_canvas.axes.set_ylabel(y_label)
        self.mpl_canvas.axes.plot(x, y)
        self.mpl_canvas.axes.yaxis.grid()
        self.mpl_canvas.axes.xaxis.grid()
        self.mpl_canvas.draw()
