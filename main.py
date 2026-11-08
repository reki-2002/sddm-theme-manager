
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


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
            "Manage your SDDM themes easily."
        )

        button = QPushButton("Scan installed themes")
        button.clicked.connect(self.scan_themes)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(button)
        layout.addStretch()

        self.setCentralWidget(container)

    def scan_themes(self):
        print("Theme scanning will be implemented next!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ThemeManager()
    window.show()

    sys.exit(app.exec())
