import sys

from PySide6.QtWidgets import QApplication, QMessageBox

import logging

log = logging.getLogger(__name__)


def show_qt_questionbox(*, title: str, message: str):
    """
    Launch a PySide6 application to show a question box dialog.

    Parameters
    ----------
    title
        Title of the message dialog
    message
        Actual message
    """
    app = QApplication(sys.argv)

    dlg = QMessageBox()

    dlg.setWindowTitle(title)
    dlg.setText(message)
    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    dlg.setIcon(QMessageBox.Question)

    button_clicked = dlg.exec_()
    return button_clicked == QMessageBox.Yes


# app.exec_()
