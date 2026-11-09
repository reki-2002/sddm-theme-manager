import sys
import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QMessageBox,
    QStackedWidget
)

from src.core.theme_scanner import scan_themes
from src.widgets.theme_card import ThemeCard
from src.widgets.theme_details import ThemeDetails
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class ThemeManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDDM Theme Manager")
        self.resize(1100, 750)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        # Gallery page
        self.gallery_page = QWidget()
        self.gallery_layout = QVBoxLayout(self.gallery_page)

        title = QLabel("SDDM Theme Manager")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        description = QLabel(
            "Explore your installed SDDM themes."
        )
        self.open_themes_button = QPushButton("📂 Open Themes Folder")
        
        self.open_themes_button.clicked.connect(
            self.open_themes_folder
            
        )

        refresh_button = QPushButton("Refresh themes")
        refresh_button.clicked.connect(self.load_themes)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.status = QLabel("Ready.")

        self.gallery_layout.addWidget(title)
        self.gallery_layout.addWidget(description)
        self.gallery_layout.addWidget(self.open_themes_button)
        self.gallery_layout.addWidget(refresh_button)
        self.gallery_layout.addWidget(self.scroll, 1)
        self.gallery_layout.addWidget(self.status)

        # Details page
        self.details_page = ThemeDetails()
        self.details_page.back_requested.connect(
            self.show_gallery
        )

        self.pages.addWidget(self.gallery_page)
        self.pages.addWidget(self.details_page)

        self.load_themes()
    
    def open_themes_folder(self):
        themes_path = Path("/usr/share/sddm/themes")
        
        if not themes_path.is_dir():
            QMessageBox.warning(
                self,
                "Folder not found",
                "The SDDM themes directory does not exist."
            )
            return
        
        try:
            subprocess.Popen(
                ["xdg-open", str(themes_path)]
            )
        except OSError as error:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open the themes folder:\n{error}"
            )

    def load_themes(self):
        try:
            themes = scan_themes()
        except OSError as error:
            QMessageBox.warning(
                self, "Scan failed", str(error)
            )
            return

        gallery = QWidget()
        gallery_layout = QVBoxLayout(gallery)

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
        self.details_page.load_theme(theme)
        self.pages.setCurrentWidget(self.details_page)

    def show_gallery(self):
        self.load_themes()
        self.pages.setCurrentWidget(self.gallery_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ThemeManager()
    window.show()

    sys.exit(app.exec())
