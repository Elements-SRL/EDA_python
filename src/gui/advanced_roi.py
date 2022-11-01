from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src.metadata.data_classes.data_group import DataGroup
from src.analysis.fitting.FittingParams import FittingParams


class AdvancedRoiWidget(QWidget):

    def __init__(self, dg: DataGroup):
        super(AdvancedRoiWidget, self).__init__()
        self.channels_checked = True
        self.sweeps_checked = True
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
        self.sweeps_checkbox: List[QCheckBox] = []
        select_unselect_channels_button = QPushButton("Select/Unselect all channels")
        select_unselect_channels_button.pressed.connect(lambda: self.select_unselect_all_channels())
        outer_layout.addWidget(select_unselect_channels_button)
        sweep_label = QLabel("Select sweeps to keep")
        outer_layout.addWidget(sweep_label)
        for sweep_number in range(dg.sweep_count):
            sweep = QCheckBox("sweep: " + str(sweep_number))
            sweep.setChecked(True)
            outer_layout.addWidget(sweep)
            self.sweeps_checkbox.append(sweep)
        select_unselect_sweeps_button = QPushButton("Select/Unselect all sweeps")
        select_unselect_sweeps_button.pressed.connect(lambda: self.select_unselect_all_sweeps())
        outer_layout.addWidget(select_unselect_sweeps_button)
        self.create_roi_button = QPushButton("Create ROI")
        # TODO add button select/unselect all channels and sweeps
        outer_layout.addWidget(self.create_roi_button)
        self.show()

    def select_unselect_all_channels(self):
        self.channels_checked = not self.channels_checked
        for cb in self.channels_checkbox:
            cb.setChecked(self.channels_checked)
    
    def select_unselect_all_sweeps(self):
        self.sweeps_checked = not self.sweeps_checked
        for cb in self.sweeps_checkbox:
            cb.setChecked(self.sweeps_checked)