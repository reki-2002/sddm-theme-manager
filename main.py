
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
)

from src.core.theme_scanner import scan_themes


class ThemeManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDDM Theme Manager")
        self.resize(900, 600)

        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel("SDDM Theme Manager")
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
        )

        description = QLabel(
            "Manage your installed SDDM themes."
        )

        self.scan_button = QPushButton(
            "Scan installed themes"
        )
        self.scan_button.clicked.connect(
            self.load_themes
        )

        self.theme_list = QListWidget()

        self.status = QLabel("Ready to scan.")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.theme_list)
        layout.addWidget(self.status)

        self.setCentralWidget(container)

        self.load_themes()

    def load_themes(self):
        self.theme_list.clear()

        try:
            themes = scan_themes()
        except OSError as error:
            QMessageBox.warning(
                self,
                "Scan failed",
                str(error)
            )
            return

        for theme in themes:
            self.theme_list.addItem(
                f"{theme['name']} ({theme['id']})"
            )

        self.status.setText(
            f"{len(themes)} installed theme(s) found."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ThemeManager()
    window.show()

    sys.exit(app.exec())
