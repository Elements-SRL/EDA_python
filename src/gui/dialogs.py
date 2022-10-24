from PyQt5.QtWidgets import QMessageBox


def show_empty_abfs_dialog(title, text, informative_text):
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowTitle(title)
    message_box.setInformativeText(informative_text)
    message_box.exec()


def show_warning(title, text, msg):
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Warning)
    message_box.setWindowTitle(title)
    message_box.setInformativeText(msg)
    message_box.exec()
