
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QPushButton, QFrame
)


class ScreenshotThumbnail(QWidget):
    selected = Signal(int)
    remove_requested = Signal(int)

    def __init__(self, path, index, removable=False, parent=None):
        super().__init__(parent)

        self.index = index
        self.setFixedSize(132, 82)
        self.setMouseTracking(True)

        self.preview_button = QPushButton(self)
        self.preview_button.setGeometry(0, 0, 132, 82)
        self.preview_button.setIconSize(QSize(120, 70))
        self.preview_button.clicked.connect(
            lambda: self.selected.emit(self.index)
        )

        pixmap = QPixmap(path)

        if not pixmap.isNull():
            thumbnail = pixmap.scaled(
                120, 70,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview_button.setIcon(QIcon(thumbnail))
        else:
            self.preview_button.setText("Unavailable")

        self.remove_button = QPushButton("×", self)
        self.remove_button.setGeometry(106, 4, 22, 22)
        self.remove_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #d94343;
                color: white;
                border: none;
                border-radius: 11px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #ff5555;
            }
        """)

        self.remove_button.clicked.connect(
            lambda: self.remove_requested.emit(self.index)
        )

        self.removable = removable
        self.remove_button.hide()

    def enterEvent(self, event):
        if self.removable:
            self.remove_button.show()
            self.remove_button.raise_()

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.remove_button.hide()
        super().leaveEvent(event)

    def set_selected(self, selected):
        if selected:
            self.preview_button.setStyleSheet(
                "border: 2px solid #4285f4;"
                "border-radius: 6px;"
            )
        else:
            self.preview_button.setStyleSheet("")
