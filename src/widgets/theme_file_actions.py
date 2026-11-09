
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox
)


class ThemeFileActions(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.theme_path = None

        layout = QVBoxLayout(self)

        self.path_label = QLabel("No theme selected")
        self.path_label.setWordWrap(True)
        self.path_label.setTextInteractionFlags(
            self.path_label.textInteractionFlags()
        )

        buttons = QHBoxLayout()

        self.open_button = QPushButton("Open Folder")
        self.copy_button = QPushButton("Copy Path")

        self.open_button.clicked.connect(self.open_folder)
        self.copy_button.clicked.connect(self.copy_path)

        buttons.addWidget(self.open_button)
        buttons.addWidget(self.copy_button)

        layout.addWidget(self.path_label)
        layout.addLayout(buttons)

        self.open_button.setEnabled(False)
        self.copy_button.setEnabled(False)

    def set_theme(self, theme):
        path = theme.get("path")

        self.theme_path = Path(path) if path else None

        self.path_label.setText(
            str(self.theme_path)
            if self.theme_path else "Path unavailable"
        )

        self.open_button.setEnabled(bool(self.theme_path))
        self.copy_button.setEnabled(bool(self.theme_path))

    def open_folder(self):
        if not self.theme_path or not self.theme_path.is_dir():
            QMessageBox.warning(
                self, "Folder unavailable",
                "The theme directory does not exist."
            )
            return

        if not QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(self.theme_path))
        ):
            QMessageBox.warning(
                self, "Open failed",
                "Could not open the theme directory."
            )

    def copy_path(self):
        if self.theme_path:
            QGuiApplication.clipboard().setText(
                str(self.theme_path)
            )
            self.copy_button.setText("Copied!")
