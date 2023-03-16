from typing import Tuple

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDoubleSpinBox, QLabel, QMessageBox

MIN_VALUE = 1
MAX_VALUE = 1000


class DwellAnalysisWidget(QWidget):
    def __init__(self):
        super(DwellAnalysisWidget, self).__init__()
        views_layout = QVBoxLayout()
        self.setWindowTitle("Dwell Analysis")
        self.setLayout(views_layout)

        views_layout.addWidget(QLabel("Minimum event duration"))
        # TODO set min and max values for qdoublespinbox
        self.min_event_duration_spin_box = QDoubleSpinBox()
        self.min_event_duration_spin_box.setMinimum(MIN_VALUE)
        self.min_event_duration_spin_box.setMaximum(MAX_VALUE)
        self.min_event_duration_spin_box.setValue(10)
        views_layout.addWidget(self.min_event_duration_spin_box)

        views_layout.addWidget(QLabel("Maximum event duration"))
        self.max_event_length_spin_box = QDoubleSpinBox()
        self.max_event_length_spin_box.setMinimum(MIN_VALUE)
        self.max_event_length_spin_box.setMaximum(MAX_VALUE)
        self.max_event_length_spin_box.setValue(100)

        views_layout.addWidget(self.max_event_length_spin_box)

        self.extract_event_push_button = QPushButton("Extract events")
        views_layout.addWidget(self.extract_event_push_button)
        self.show()

    def get_push_button(self) -> QPushButton:
        return self.extract_event_push_button

    def get_values(self) -> Tuple[float, float]:
        return self.min_event_duration_spin_box.value(), self.max_event_length_spin_box.value()

