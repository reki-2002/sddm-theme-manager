
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QMessageBox
)

from src.core.theme_scanner import scan_themes
from src.widgets.theme_card import ThemeCard
from src.widgets.theme_details import ThemeDetails


class ThemeManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDDM Theme Manager")
        self.resize(1000, 700)

        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("SDDM Theme Manager")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")

        description = QLabel("Explore your installed SDDM themes.")

        scan_button = QPushButton("Refresh themes")
        scan_button.clicked.connect(self.load_themes)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.status = QLabel("Ready.")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(scan_button)
        layout.addWidget(self.scroll, 1)
        layout.addWidget(self.status)

        self.setCentralWidget(container)
        self.load_themes()

    def load_themes(self):
        try:
            themes = scan_themes()
        except OSError as error:
            QMessageBox.warning(self, "Scan failed", str(error))
            return

        gallery = QWidget()
        gallery_layout = QVBoxLayout(gallery)

        # Simple rows of three cards.
        for start in range(0, len(themes), 3):
            row = QHBoxLayout()

            for theme in themes[start:start + 3]:
                card = ThemeCard(theme)
                card.clicked.connect(self.open_details)
                row.addWidget(card)

            row.addStretch()
            gallery_layout.addLayout(row)

        gallery_layout.addStretch()

        self.scroll.setWidget(gallery)
        self.status.setText(
            f"{len(themes)} installed theme(s) found."
        )

    def open_details(self, theme):
        dialog = ThemeDetails(theme, self)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ThemeManager()
    window.show()

    sys.exit(app.exec())
