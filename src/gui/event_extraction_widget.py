from typing import Tuple, List

import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QScrollArea
from src.constants.strings import *
from src.gui.filters_widget import MplCanvas


class EventExtractionWidget(QWidget):
    def __init__(self, events: List[Tuple[float, float, int, int]], measuring_unit: str):
        super(EventExtractionWidget, self).__init__()
        self.mpl_canvas = MplCanvas()
        self.events = events
        outer_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        plot_layout = QVBoxLayout()
        scrollable_widget = QWidget()
        scroll_area = QScrollArea()
        scrollable_layout = QHBoxLayout()
        amplitudes_layout = QVBoxLayout()
        durations_layout = QVBoxLayout()
        begins_layout = QVBoxLayout()
        ends_layout = QVBoxLayout()

        amplitudes_layout.addWidget(QLabel(AMPLITUDE_LABEL))
        durations_layout.addWidget(QLabel(DURATION_LABEL))
        begins_layout.addWidget(QLabel(START_OF_EVENT_LABEL))
        ends_layout.addWidget(QLabel(END_OF_EVENT_LABEL))
        self.setWindowTitle(EXTRACTED_EVENTS_LABEL)
        amplitudes = np.array([e[0] for e in events])
        durations = np.array([e[1] for e in events])
        self.mpl_canvas.axes.scatter(durations, amplitudes)
        self.mpl_canvas.axes.set_xlabel('Half width (s)')
        self.mpl_canvas.axes.set_ylabel('Amplitude ' + measuring_unit)
        self.mpl_canvas.axes.yaxis.grid()
        self.mpl_canvas.axes.xaxis.grid()
        for a, d, b, e in events:
            amplitudes_layout.addWidget(_create_disabled_line_edit(a))
            durations_layout.addWidget(_create_disabled_line_edit(d))
            begins_layout.addWidget(_create_disabled_line_edit(b))
            ends_layout.addWidget(_create_disabled_line_edit(e))
        scrollable_layout.addLayout(amplitudes_layout)
        scrollable_layout.addLayout(durations_layout)
        scrollable_layout.addLayout(begins_layout)
        scrollable_layout.addLayout(ends_layout)
        scrollable_widget.setLayout(scrollable_layout)
        scroll_area.setWidget(scrollable_widget)
        horizontal_layout.addWidget(scroll_area)
        # The following commented lines do not work
        # toolbar = NavigationToolbar(self.mpl.axes)
        # plot_layout.addWidget(toolbar)
        plot_layout.addWidget(self.mpl_canvas)
        horizontal_layout.addLayout(plot_layout)
        outer_layout.addLayout(horizontal_layout)

        self.export_to_csv_button = QPushButton("Export to csv")
        outer_layout.addWidget(self.export_to_csv_button)
        self.setLayout(outer_layout)
        self.show()

    def get_push_button(self) -> QPushButton:
        return self.export_to_csv_button

    def get_events(self) -> List[Tuple[float, float, int, int]]:
        return self.events


def _create_disabled_line_edit(p) -> QLineEdit:
    line_edit = QLineEdit(str(p))
    line_edit.setReadOnly(True)
    return line_edit
