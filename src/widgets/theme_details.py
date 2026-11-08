
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea
)


class ThemeDetails(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.theme = None
        self.previews = []
        self.index = 0

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.back_button = QPushButton("← Back to Gallery")
        self.back_button.clicked.connect(self.back_requested.emit)
        layout.addWidget(self.back_button)

        self.title = QLabel()
        self.title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )
        layout.addWidget(self.title)

        self.image = QLabel("No preview available")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumHeight(320)
        layout.addWidget(self.image, 1)

        navigation = QHBoxLayout()

        self.previous_button = QPushButton("← Previous")
        self.next_button = QPushButton("Next →")

        self.previous_button.clicked.connect(
            lambda: self.change_image(-1)
        )
        self.next_button.clicked.connect(
            lambda: self.change_image(1)
        )

        navigation.addWidget(self.previous_button)
        navigation.addStretch()
        navigation.addWidget(self.next_button)
        layout.addLayout(navigation)

        self.description = QLabel()
        self.description.setWordWrap(True)
        layout.addWidget(self.description)

        self.author = QLabel()
        layout.addWidget(self.author)

        self.install_button = QPushButton("Installed")
        self.install_button.setEnabled(False)
        layout.addWidget(self.install_button)

    def load_theme(self, theme):
        self.theme = theme
        self.previews = theme.get("previews", [])
        self.index = 0

        self.title.setText(theme["name"])
        self.description.setText(
            theme.get("description") or "No description available."
        )
        self.author.setText(
            f"Author: {theme.get('author') or 'Unknown'}"
        )

        has_multiple = len(self.previews) > 1
        self.previous_button.setEnabled(has_multiple)
        self.next_button.setEnabled(has_multiple)

        self.show_preview()

    def show_preview(self):
        self.image.clear()

        if not self.previews:
            self.image.setText("No preview available")
            return

        pixmap = QPixmap(self.previews[self.index])

        if pixmap.isNull():
            self.image.setText("Preview unavailable")
            return

        self.image.setPixmap(
            pixmap.scaled(
                780, 430,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def change_image(self, direction):
        if not self.previews:
            return

        self.index = (
            self.index + direction
        ) % len(self.previews)

        self.show_preview()
