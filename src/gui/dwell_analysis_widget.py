from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDoubleSpinBox, QLabel, QMessageBox

MIN_VALUE = 1
MAX_VALUE = 500


def show_dwell_analysis_widget(_dwell_analysis) -> QWidget:
    widget = QWidget()

    views_layout = QVBoxLayout()
    widget.setWindowTitle("Dwell Analysis")
    widget.setLayout(views_layout)
    views_layout.deleteLater()

    views_layout.addWidget(QLabel("Minimum event duration"))
    # TODO set min and max values for qdoublespinbox
    min_event_duration_spin_box = QDoubleSpinBox()
    min_event_duration_spin_box.setMinimum(MIN_VALUE)
    min_event_duration_spin_box.setMaximum(MAX_VALUE)
    min_event_duration_spin_box.setValue(10)
    views_layout.addWidget(min_event_duration_spin_box)

    views_layout.addWidget(QLabel("Maximum event duration"))
    max_event_length_spin_box = QDoubleSpinBox()
    max_event_length_spin_box.setMinimum(MIN_VALUE)
    max_event_length_spin_box.setMaximum(MAX_VALUE)
    max_event_length_spin_box.setValue(100)

    views_layout.addWidget(max_event_length_spin_box)

    extract_event_push_button = QPushButton("Extract events")
    extract_event_push_button.clicked.connect(
        lambda: _push_button_handler(_dwell_analysis, min_event_duration_spin_box.value(),
                                     max_event_length_spin_box.value(), widget))
    views_layout.addWidget(extract_event_push_button)
    widget.show()
    return widget


def _push_button_handler(dwell_analysis_func, min_event_length, max_event_length, widget):
    widget.close()
    if not dwell_analysis_func(min_event_length, max_event_length):
        message_box = QMessageBox()
        message_box.setText("The analysis did not yield any result")
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("Unsuccessful analysis")
        message_box.setInformativeText("With these parameters no event has been found, try to change some values and rerun the analysis")
        message_box.exec()

