
from PySide6.QtCore import Qt, Signal, QTimer, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea,
    QFrame, QSizePolicy, QFileDialog, QMessageBox
)
from src.core.screenshot_manager import add_screenshots
from src.core.theme_scanner import find_previews
from pathlib import Path
from src.widgets.screenshot_thumbnail import ScreenshotThumbnail
from src.core.screenshot_manager import (
    get_custom_screenshots,
    remove_screenshot
)
from src.widgets.theme_file_actions import ThemeFileActions


class ThemeDetails(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.theme = None
        self.previews = []
        self.index = 0
        self.thumbnail_buttons = []

        # Automatic slideshow
        self.timer = QTimer(self)
        self.timer.setInterval(4000)
        self.timer.timeout.connect(self.next_image)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.back_button = QPushButton("← Back to Gallery")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.title = QLabel()
        self.title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )
        layout.addWidget(self.title)

        # Main preview
        self.image = QLabel("No preview available")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumHeight(280)
        self.image.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.image, 1)

        # Navigation
        navigation = QHBoxLayout()

        self.previous_button = QPushButton("← Previous")
        self.next_button = QPushButton("Next →")

        self.previous_button.clicked.connect(
            lambda: self.change_image(-1)
        )
        self.next_button.clicked.connect(
            lambda: self.change_image(1)
        )

        self.counter = QLabel()
        self.counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        navigation.addWidget(self.previous_button)
        navigation.addStretch()
        navigation.addWidget(self.counter)
        navigation.addStretch()
        navigation.addWidget(self.next_button)

        layout.addLayout(navigation)

        # Scrollable thumbnail strip
        self.thumbnail_area = QScrollArea()
        self.thumbnail_area.setWidgetResizable(True)
        self.thumbnail_area.setFixedHeight(100)
        self.thumbnail_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.thumbnail_container = QWidget()
        self.thumbnail_layout = QHBoxLayout(
            self.thumbnail_container
        )
        self.thumbnail_layout.setContentsMargins(4, 4, 4, 4)
        self.thumbnail_layout.setSpacing(8)

        self.thumbnail_area.setWidget(
            self.thumbnail_container
        )
        layout.addWidget(self.thumbnail_area)
        self.add_screenshots_button = QPushButton(
            "+ Add Screenshots"
        )
        self.add_screenshots_button.clicked.connect(
            self.add_custom_screenshots
        )
        layout.addWidget(self.add_screenshots_button)

        self.description = QLabel()
        self.description.setWordWrap(True)
        layout.addWidget(self.description)

        self.author = QLabel()
        layout.addWidget(self.author)

        self.install_button = QPushButton("Installed")
        self.install_button.setEnabled(False)
        layout.addWidget(self.install_button)
        self.file_actions = ThemeFileActions()
        layout.addWidget(self.file_actions)

        self.update_controls()

    def load_theme(self, theme):
        self.timer.stop()

        self.theme = theme
        self.file_actions.set_theme(theme)
        self.previews = theme.get("previews", [])
        self.index = 0

        self.title.setText(theme["name"])
        self.description.setText(
            theme.get("description") or
            "No description available."
        )
        self.author.setText(
            f"Author: {theme.get('author') or 'Unknown'}"
        )

        self.create_thumbnails()
        self.update_controls()
        self.show_preview()

        if len(self.previews) > 1:
            self.timer.start()


    def add_custom_screenshots(self):
        if not self.theme:
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select screenshots",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if not files:
            return

        try:
            added = add_screenshots(
                self.theme["id"],
                files
            )

            if not added:
                QMessageBox.warning(
                    self,
                    "No images added",
                    "No valid screenshots were selected."
                )
                return

            # Reload original and custom screenshots.
            from src.core.screenshot_manager import (
                get_custom_screenshots
            )

            original = find_previews(
                Path(self.theme["path"])
            )

            self.previews = (
                original
                + get_custom_screenshots(self.theme["id"])
            )

            self.theme["previews"] = self.previews
            self.index = 0

            self.create_thumbnails()
            self.update_controls()
            self.show_preview()
            self.restart_timer()

            QMessageBox.information(
                self,
                "Screenshots added",
                f"Successfully added {len(added)} screenshot(s)."
            )

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Import failed",
                str(error)
            )
    def create_thumbnails(self):
        while self.thumbnail_layout.count():
            item = self.thumbnail_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.thumbnail_buttons.clear()

        custom_screenshots = set(
            get_custom_screenshots(self.theme["id"])
        )

        for index, path in enumerate(self.previews):
            thumbnail = ScreenshotThumbnail(
                path=path,
                index=index,
                removable=path in custom_screenshots
            )

            thumbnail.selected.connect(self.select_image)
            thumbnail.remove_requested.connect(
                self.remove_custom_screenshot
            )

            self.thumbnail_layout.addWidget(thumbnail)
            self.thumbnail_buttons.append(thumbnail)

        self.thumbnail_layout.addStretch()

    def show_preview(self):
        self.image.clear()

        if not self.previews:
            self.image.setText("No preview available")
            self.counter.setText("")
            return

        pixmap = QPixmap(self.previews[self.index])

        if pixmap.isNull():
            self.image.setText("Preview unavailable")
        else:
            available_size = self.image.size()

            if available_size.width() > 0 and available_size.height() > 0:
                self.image.setPixmap(
                    pixmap.scaled(
                        available_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )

                self.counter.setText(
            f"{self.index + 1} / {len(self.previews)}"
        )

                self.counter.setText(
            f"{self.index + 1} / {len(self.previews)}"
        )

        self.update_thumbnail_selection()

    def update_thumbnail_selection(self):
        for index, thumbnail in enumerate(self.thumbnail_buttons):
            thumbnail.set_selected(index == self.index)

    def update_controls(self):
        has_multiple = len(self.previews) > 1

        self.previous_button.setEnabled(has_multiple)
        self.next_button.setEnabled(has_multiple)

        self.thumbnail_area.setVisible(
            len(self.previews) > 0
        )

    def select_image(self, index):
        if 0 <= index < len(self.previews):
            self.index = index
            self.show_preview()
            self.restart_timer()

    def change_image(self, direction):
        if len(self.previews) <= 1:
            return

        self.index = (
            self.index + direction
        ) % len(self.previews)

        self.show_preview()
        self.restart_timer()

    def next_image(self):
        if len(self.previews) <= 1:
            return

        self.index = (self.index + 1) % len(self.previews)
        self.show_preview()

    def restart_timer(self):
        if len(self.previews) > 1:
            self.timer.start()

    def go_back(self):
        self.timer.stop()
        self.back_requested.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.previews:
            self.show_preview()

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)

    def showEvent(self, event):
        super().showEvent(event)

        if len(self.previews) > 1:
            self.timer.start()


    def remove_custom_screenshot(self, index):
        if not self.theme:
            return

        if not 0 <= index < len(self.previews):
            return

        path = self.previews[index]

        confirmation = QMessageBox.question(
            self,
            "Remove Screenshot",
            "Do you want to remove this screenshot?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            remove_screenshot(self.theme["id"], path)

            self.previews.pop(index)
            self.theme["previews"] = self.previews

            if self.previews:
                self.index = min(
                    self.index,
                    len(self.previews) - 1
                )
            else:
                self.index = 0

            self.create_thumbnails()
            self.update_controls()
            self.show_preview()

            if len(self.previews) > 1:
                self.timer.start()
            else:
                self.timer.stop()

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Removal failed",
                str(error)
            )
