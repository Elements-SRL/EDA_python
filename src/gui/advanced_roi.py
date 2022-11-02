from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from src.metadata.data_classes.data_group import DataGroup
from src.analysis.fitting.FittingParams import FittingParams
from typing import Tuple, List

class AdvancedRoiWidget(QWidget):

    def __init__(self, dg: DataGroup):
        super(AdvancedRoiWidget, self).__init__()
        self.dg = dg
        self.channels_checked = True
        self.sweeps_checked = True
        outer_div = QVBoxLayout()
        cols_div = QHBoxLayout()
        outer_div.addLayout(cols_div)
        first_col = QVBoxLayout()
        second_col = QVBoxLayout()
        cols_div.addLayout(first_col)
        cols_div.addLayout(second_col)
        self.setLayout(outer_div)
        self.setWindowTitle("Advanced ROI")
        self.setMinimumSize(200, 300)
        # First col
        self.channels_checkbox: List[QCheckBox] = []
        channels_label = QLabel("Select channels to keep")
        first_col.addWidget(channels_label)
        for ch_number in [bd.ch for bd in dg.basic_data ]:
            ch = QCheckBox("channel: " + str(ch_number))
            ch.setChecked(True)
            first_col.addWidget(ch)
            self.channels_checkbox.append(ch)
        self.sweeps_checkbox: List[QCheckBox] = []
        select_unselect_channels_button = QPushButton("Select/Unselect all channels")
        select_unselect_channels_button.pressed.connect(lambda: self._select_unselect_all_channels())
        first_col.addWidget(select_unselect_channels_button)
        sweep_label = QLabel("Select sweeps to keep")
        first_col.addWidget(sweep_label)
        for sweep_number in range(dg.sweep_count):
            sweep = QCheckBox("sweep: " + str(sweep_number))
            sweep.setChecked(True)
            first_col.addWidget(sweep)
            self.sweeps_checkbox.append(sweep)
        select_unselect_sweeps_button = QPushButton("Select/Unselect all sweeps")
        select_unselect_sweeps_button.pressed.connect(lambda: self._select_unselect_all_sweeps())
        first_col.addWidget(select_unselect_sweeps_button)

        # Second col
        x_min = dg.x.min()
        x_max = dg.x.max()
        self.x_min_label = QLabel("From x value of:")
        self.x_min_spin_box = QDoubleSpinBox()
        self.x_min_spin_box = QDoubleSpinBox()
        self.x_min_spin_box.setMinimum(x_min)
        self.x_min_spin_box.setMaximum(x_max)
        self.x_min_spin_box.setValue(x_min)

        second_col.addWidget(self.x_min_label)
        second_col.addWidget(self.x_min_spin_box)

        self.x_max_label = QLabel("To x value of:")
        self.x_max_spin_box = QDoubleSpinBox()
        self.x_max_spin_box = QDoubleSpinBox()
        self.x_max_spin_box.setMinimum(x_min)
        self.x_max_spin_box.setMaximum(x_max)
        self.x_max_spin_box.setValue(x_max)
        second_col.addWidget(self.x_max_label)
        second_col.addWidget(self.x_max_spin_box)


        # Outer div
        self.create_roi_button = QPushButton("Create ROI")
        # TODO add button select/unselect all channels and sweeps
        outer_div.addWidget(self.create_roi_button)
        self.show()

    def _select_unselect_all_channels(self):
        self.channels_checked = not self.channels_checked
        for cb in self.channels_checkbox:
            cb.setChecked(self.channels_checked)
    
    def _select_unselect_all_sweeps(self):
        self.sweeps_checked = not self.sweeps_checked
        for cb in self.sweeps_checkbox:
            cb.setChecked(self.sweeps_checked)

    def get_x_values(self) -> Tuple[int, int]:
        return self.x_min_spin_box.value(), self.x_max_spin_box.value()
    
    def get_sweeps_to_keep(self) -> List[int]:
        return [int(cb.text().split(" ").pop()) for cb in self.sweeps_checkbox if cb.isChecked()]
    
    def get_channels_to_keep(self) -> List[int]:
        return [int(cb.text().split(" ").pop()) for cb in self.channels_checkbox if cb.isChecked()]