from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: black;")

        self.label = QLabel(self)
        self.pixmap = QPixmap("graphics/logo.jpg")
        self.label.setPixmap(self.pixmap)

        # Ensure the image scales with the label
        self.label.setScaledContents(True)

        self.showMaximized()

    def resizeEvent(self, event):
        """Adjust label size when window is resized."""
        self.label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())