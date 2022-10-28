from typing import Iterable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from src.analysis.fitting.FittingParams import FittingParams


class FittingParamsWidget(QWidget):

    def __init__(self, equation: str, fitting_params: Iterable[FittingParams]):
        super(FittingParamsWidget, self).__init__()
        self.equation = equation
        self.fitting_params: Iterable[FittingParams] = fitting_params
        outer_layout = QVBoxLayout()
        self.setWindowTitle("Fitting Params")
        self.setMinimumSize(200, 300)
        self.setLayout(outer_layout)
        scroll_widget = QWidget()
        scroll_widget.setMinimumSize(200, 300)
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        name_col = QVBoxLayout()
        value_col = QVBoxLayout()
        column_container = QHBoxLayout()
        column_container.addLayout(name_col)
        column_container.addLayout(value_col)
        name_col.addWidget(QLabel("Equation:"))
        qle = QLineEdit(self.equation)
        qle.setReadOnly(True)
        qle.setMinimumWidth(200)
        value_col.addWidget(qle)

        for fp in fitting_params:
            name_col.addWidget(QLabel("channel"))
            qle = QLineEdit(str(fp.ch))
            qle.setReadOnly(True)
            value_col.addWidget(qle)
            name_col.addWidget(QLabel("measuring unit"))
            value_col.addWidget(QLineEdit(fp.measuring_unit))
            for p in fp.popt:
                name, value = p
                name_col.addWidget(QLabel(name))
                qle = QLineEdit(str(value))
                qle.setReadOnly(True)
                value_col.addWidget(qle)
        scroll_widget.setLayout(column_container)
        scroll_area.setWidget(scroll_widget)
        outer_layout.addWidget(scroll_area)
        self.export_button = QPushButton("Export value to csv")
        outer_layout.addWidget(self.export_button)
        self.show()
