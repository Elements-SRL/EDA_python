from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src.metadata.data_classes.data_group import DataGroup
from src.analysis.fitting.FittingParams import FittingParams


class AdvancedRoiWidget(QWidget):

    def __init__(self, dg: DataGroup):
        super(AdvancedRoiWidget, self).__init__()
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)
        self.setWindowTitle("Advanced ROI")
        self.setMinimumSize(200, 300)
        self.channels_checkbox: List[QCheckBox] = []
        for bd in dg.basic_data:
            ch = QCheckBox("channel: " + str(bd.ch))
            ch.setChecked(True)
            outer_layout.addWidget(ch)
            self.channels_checkbox.append(ch)
        self.create_roi_button = QPushButton("Create ROI")
        outer_layout.addWidget(self.create_roi_button)
        self.show()
