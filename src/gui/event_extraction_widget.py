from typing import Tuple, List

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QScrollArea


class EventExtractionWidget(QWidget):
    def __init__(self, events: List[Tuple[float, int, int, int]]):
        super(EventExtractionWidget, self).__init__()
        outer_layout = QVBoxLayout()
        scrollable_widget = QWidget()
        scroll_area = QScrollArea()
        scrollable_layout = QHBoxLayout()
        amplitudes_layout = QVBoxLayout()
        durations_layout = QVBoxLayout()
        begins_layout = QVBoxLayout()
        ends_layout = QVBoxLayout()

        amplitudes_layout.addWidget(QLabel("Amplitudes"))
        durations_layout.addWidget(QLabel("Durations"))
        begins_layout.addWidget(QLabel("Start of event"))
        ends_layout.addWidget(QLabel("End of event"))
        self.setWindowTitle("Extracted events")
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
        outer_layout.addWidget(scroll_area)

        export_to_csv_button = QPushButton("Export to csv")
        outer_layout.addWidget(export_to_csv_button)
        self.setLayout(outer_layout)
        self.show()


def _create_disabled_line_edit(p) -> QLineEdit:
    line_edit = QLineEdit(str(p))
    line_edit.setReadOnly(True)
    return line_edit
