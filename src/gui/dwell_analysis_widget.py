from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDoubleSpinBox
from src.metadata.data_classes.data_group import DataGroup


def show_views_widget(data_group: DataGroup, _dwell_analysis) -> QWidget:
    views_widget = QWidget()

    views_layout = QVBoxLayout()
    views_widget.setWindowTitle("Dwell Analysis")
    # views_widget.setMinimumSize(200, 300)
    views_widget.setLayout(views_layout)
    views_layout.deleteLater()

    # TODO set min and max values for qdoublespinbox
    min_event_duration_spin_box = QDoubleSpinBox()
    max_event_length_spin_box = QDoubleSpinBox()

    views_layout.addWidget(min_event_duration_spin_box)
    views_layout.addWidget(max_event_length_spin_box)

    extract_event_push_button = QPushButton("Extract events")
    extract_event_push_button.clicked.connect(
        lambda: _dwell_analysis(data_group, min_event_duration_spin_box.value(), max_event_length_spin_box.value()))
    views_layout.addWidget(extract_event_push_button)
    views_widget.show()
    return views_widget

