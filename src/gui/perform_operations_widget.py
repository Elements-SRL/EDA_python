import re
from typing import List

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QComboBox, QLineEdit, \
    QPushButton, QCheckBox, QMessageBox, QListWidgetItem, QFrame

from src.metadata.data_classes.basic_data import BasicData


class OperationsWidget(QWidget):
    def __init__(self, items: List[BasicData], fun):
        super().__init__()

        self.items = items
        self.init_ui()
        self.fun = fun

    def init_ui(self):
        layout = QVBoxLayout()

        # Section A
        section_a_layout = QVBoxLayout()
        section_a_header_layout = QHBoxLayout()  # New QHBoxLayout for label and content
        label_a = QLabel("a")
        help_text_a = QLabel("Choose the channel/sweep to be affected by the operation.")
        items = [bd.name for bd in self.items]
        self.list_widget = QListWidget()
        for item in items:
            list_item = QListWidgetItem(self.list_widget)
            check_box = QCheckBox(item)
            self.list_widget.setItemWidget(list_item, check_box)

        section_a_header_layout.addWidget(label_a)  # Add label to the header layout
        section_a_layout.addWidget(help_text_a)
        section_a_header_layout.addWidget(self.list_widget)  # Add list widget directly to header layout

        section_a_layout.addLayout(section_a_header_layout)  # Add header layout to section layout
        layout.addLayout(section_a_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Section B
        section_b_layout = QVBoxLayout()
        section_b_header_layout = QHBoxLayout()  # New QHBoxLayout for label and content
        label_b = QLabel("b")
        help_text_b = QLabel("Choose the other channel/sweep.")

        self.combo_box = QComboBox()
        self.combo_box.addItems(items)

        section_b_header_layout.addWidget(label_b)  # Add label to the header layout
        section_b_layout.addWidget(help_text_b)
        section_b_header_layout.addStretch()  # Add stretch to push label to the left
        section_b_header_layout.addWidget(self.combo_box)  # Add combo box to the header layout

        section_b_layout.addLayout(section_b_header_layout)  # Add header layout to section layout
        layout.addLayout(section_b_layout)

        # Text Field
        help_text_field = QLabel("Enter a string using 'a', 'b', and operators (+, -, *, /). Example: 'a+b-a'.")
        help_text_field2 = QLabel(" - The operations will be computed in order from left to right (not following the standard operator precedence)")
        help_text_field4 = QLabel(" - Parentheses are not allowed")
        layout.addWidget(help_text_field)
        layout.addWidget(help_text_field2)
        layout.addWidget(help_text_field4)
        self.text_field = QLineEdit()
        layout.addWidget(self.text_field)

        # Buttons
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect button clicks to functions
        # self.apply_button.clicked.connect(self.apply_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

    def apply_clicked(self) -> bool:
        input_text = self.text_field.text()
        regex_pattern = r'^[ab]([+\-*/][ab])*[+\-*/]*$'

        if re.match(regex_pattern, input_text):
            self.close()
            self.fun(self.get_selected_checkbox_basic_data(), self.get_selected_combobox_basic_data(),  input_text)
            return True
        else:
            QMessageBox.warning(self, "Validation", "Input is not valid. Please follow the specified pattern.")
            return False

    def get_selected_checkbox_basic_data(self) -> List[BasicData]:
        selected_indexes = [
            idx
            for idx in range(self.list_widget.count())
            if self.list_widget.itemWidget(self.list_widget.item(idx)).isChecked()
        ]
        return [self.items[idx] for idx in selected_indexes]

    def get_selected_combobox_basic_data(self) -> BasicData:
        return self.items[self.combo_box.currentIndex()]

    def get_apply_button(self):
        return self.apply_button

    def cancel_clicked(self):
        self.close()

