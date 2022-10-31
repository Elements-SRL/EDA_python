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
        channels_label = QLabel("Select channels to keep")
        outer_layout.addWidget(channels_label)
        for ch_number in range(dg.channel_count):
            ch = QCheckBox("channel: " + str(ch_number))
            ch.setChecked(True)
            outer_layout.addWidget(ch)
            self.channels_checkbox.append(ch)
        self.sweep_checkbox: List[QCheckBox] = []
        sweep_label = QLabel("Select sweeps to keep")
        outer_layout.addWidget(sweep_label)
        for sweep_number in range(dg.sweep_count):
            sweep = QCheckBox("sweep: " + str(sweep_number))
            sweep.setChecked(True)
            outer_layout.addWidget(sweep)
            self.sweep_checkbox.append(sweep)
        self.create_roi_button = QPushButton("Create ROI")
        # TODO add button select/unselect all channels and sweeps
        outer_layout.addWidget(self.create_roi_button)
        self.show()
