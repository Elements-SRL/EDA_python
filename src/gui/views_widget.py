from typing import Iterable, List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QCheckBox, QPushButton
from src.metadata.data_classes.basic_data import BasicData


def show_views_widget(basic_data: Iterable[BasicData], _hide_sweeps_func) -> QWidget:
    views_layout = QVBoxLayout()
    scroll_layout = QVBoxLayout()
    scroll_widget = QWidget()
    scroll_widget.setMinimumSize(200, 300)
    scroll_area = QScrollArea()
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    views_widget = QWidget()
    views_widget.setWindowTitle("Views")
    views_widget.setMinimumSize(200, 300)
    views_widget.setLayout(views_layout)
    checkboxes = []
    views_layout.deleteLater()
    for d in basic_data:
        b = QCheckBox(d.name)
        scroll_layout.addWidget(b)
        b.setChecked(d.visible)
        checkboxes.append(b)
    scroll_widget.setLayout(scroll_layout)
    scroll_area.setWidget(scroll_widget)
    views_layout.addWidget(scroll_area)
    apply_button = QPushButton("Show selected channels")
    apply_button.clicked.connect(lambda: _hide_sweeps_func(checkboxes))
    check_all_button = QPushButton("Check all")
    check_all_button.clicked.connect(lambda: set_all_checked(checkboxes, True))
    uncheck_all_button = QPushButton("Uncheck all")
    uncheck_all_button.clicked.connect(lambda: set_all_checked(checkboxes, False))
    views_layout.addWidget(apply_button)
    views_layout.addWidget(check_all_button)
    views_layout.addWidget(uncheck_all_button)
    views_widget.show()
    return views_widget


def set_all_checked(checkboxes: List[QCheckBox], state: bool):
    for cb in checkboxes:
        cb.setChecked(state)
