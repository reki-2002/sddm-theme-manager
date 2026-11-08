
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel
)


class ThemeCard(QFrame):
    clicked = Signal(dict)

    def __init__(self, theme):
        super().__init__()

        self.theme = theme
        self.previews = theme.get("previews", [])
        self.index = 0

        self.setObjectName("themeCard")
        self.setFixedWidth(250)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)

        self.image = QLabel("No preview available")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setFixedSize(226, 135)
        self.image.setStyleSheet(
            "background: #303744; color: white; border-radius: 6px;"
        )

        self.name = QLabel(theme["name"])
        self.name.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.description = QLabel(
            theme.get("description") or "Installed SDDM theme"
        )
        self.description.setWordWrap(True)
        self.description.setFixedHeight(42)

        layout.addWidget(self.image)
        layout.addWidget(self.name)
        layout.addWidget(self.description)

        self.setStyleSheet("""
            QFrame#themeCard {
                border: 1px solid #a0a0a0;
                border-radius: 9px;
                background: palette(window);
            }
            QFrame#themeCard:hover {
                border: 2px solid #5b9bd5;
            }
        """)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_preview)

        if self.previews:
            self.show_preview()
            if len(self.previews) > 1:
                self.timer.start(3500)

    def show_preview(self):
        pixmap = QPixmap(self.previews[self.index])
        if pixmap.isNull():
            self.image.setText("Preview unavailable")
            return

        scaled = pixmap.scaled(
            self.image.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled)

    def next_preview(self):
        self.index = (self.index + 1) % len(self.previews)
        self.show_preview()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.theme)
        super().mousePressEvent(event)
