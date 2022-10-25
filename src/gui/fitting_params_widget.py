from typing import Iterable
from PyQt5.QtWidgets import *

from src.analysis.fitting.FittingParams import FittingParams


class FittingParamsWidget(QWidget):

    def __init__(self, equation: str, fitting_params: Iterable[FittingParams]):
        super(FittingParamsWidget, self).__init__()
        self.equation = equation
        self.fitting_params:Iterable[FittingParams] = fitting_params
        outer_layout = QVBoxLayout()
        self.setWindowTitle("Fitting Params")
        self.setMinimumSize(200, 300)
        self.setLayout(outer_layout)
        name_col = QVBoxLayout()
        value_col = QVBoxLayout()
        column_container = QHBoxLayout()
        column_container.addLayout(name_col)
        column_container.addLayout(value_col)
        name_col.addWidget(QLabel("Equation:"))
        value_col.addWidget(QLabel(self.equation))
        for fp in fitting_params:
            name_col.addWidget(QLabel("channel"))
            value_col.addWidget(QLabel(str(fp.ch)))
            name_col.addWidget(QLabel("measuring unit"))
            value_col.addWidget(QLabel(fp.measuring_unit))
            for p in fp.popt:
                name, value = p
                name_col.addWidget(QLabel(name))
                value_col.addWidget(QLabel(str(value)))
        outer_layout.addLayout(column_container)
        export_button = QPushButton("Export value to csv")
        export_button.pressed.connect(lambda: self.export_to_csv())
        outer_layout.addWidget(export_button)
        self.show()

    def export_to_csv(self):
        print("ciccia")
