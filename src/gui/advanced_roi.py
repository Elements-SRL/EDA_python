from typing import Iterable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from src.analysis.fitting.FittingParams import FittingParams


class AdvancedRoiWidget(QWidget):

    def __init__(self):
        super(AdvancedRoiWidget, self).__init__()
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)
        self.setWindowTitle("Advanced ROI")
        self.setMinimumSize(200, 300)
        self.create_roi_button = QPushButton("Create ROI")
        outer_layout.addWidget(self.create_roi_button)
        self.show()
