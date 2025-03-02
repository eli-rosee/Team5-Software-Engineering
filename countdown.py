from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: black;")  

        # Label for the logo image
        self.label = QLabel(self)
        self.pixmap = QPixmap("graphics/logo.jpg")

        # Check if image loaded correctly
        if self.pixmap.isNull():
            print("Error: Image not found. Check path.")
        else:
            self.label.setPixmap(self.pixmap)

        self.label.setScaledContents(True)  # Scale image to fit label
        self.label.setGeometry(0, 0, self.width(), self.height())

        self.showMaximized()  # Make the window fullscreen

    def resizeEvent(self, event):
        """ Ensure the label resizes with the window """
        self.label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
