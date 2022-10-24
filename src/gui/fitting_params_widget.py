from typing import Tuple, List
from PyQt5.QtWidgets import *


class FittingParamsWidget(QWidget):

    def __init__(self, equation: str, params: List[Tuple[str, float]]):
        super(FittingParamsWidget, self).__init__()
        self.equation = equation
        self.params = params
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
        for p in params:
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
