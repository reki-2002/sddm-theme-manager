
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)


class ThemeDetails(QDialog):
    def __init__(self, theme, parent=None):
        super().__init__(parent)

        self.theme = theme
        self.previews = theme.get("previews", [])
        self.index = 0

        self.setWindowTitle(theme["name"])
        self.resize(850, 650)

        layout = QVBoxLayout(self)

        title = QLabel(theme["name"])
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        self.image = QLabel("No preview available")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumHeight(350)
        layout.addWidget(self.image, 1)

        navigation = QHBoxLayout()

        previous = QPushButton("Previous")
        next_button = QPushButton("Next")

        previous.clicked.connect(lambda: self.change_image(-1))
        next_button.clicked.connect(lambda: self.change_image(1))

        previous.setEnabled(len(self.previews) > 1)
        next_button.setEnabled(len(self.previews) > 1)

        navigation.addWidget(previous)
        navigation.addStretch()
        navigation.addWidget(next_button)
        layout.addLayout(navigation)

        description = QLabel(
            theme.get("description") or "No description available."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        author = QLabel(
            f"Author: {theme.get('author') or 'Unknown'}"
        )
        layout.addWidget(author)

        button = QPushButton("Installed")
        button.setEnabled(False)
        layout.addWidget(button)

        self.show_preview()

    def show_preview(self):
        if not self.previews:
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

        self.index = (self.index + direction) % len(self.previews)
        self.show_preview()
