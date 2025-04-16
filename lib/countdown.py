from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
import sys
import os

from music import music_player

class CountdownWindow(QMainWindow):
    def __init__(self, on_exit):
        super().__init__()

        self.on_exit = on_exit
        self.time_interval = 1400

        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Countdown")

        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        self.countdown_label = QLabel(self)
        self.countdown_label.setScaledContents(True)
        self.countdown_label.setGeometry(0, 0, self.width(), self.height())

        self.showMaximized()  

        self.start_countdown()

    def start_countdown(self):
        """Starts the countdown timer and updates images every second."""
        self.countdown_time = 30  
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(self.time_interval)  

    def update_countdown(self):
        """Updates the countdown image every second."""

        if (self.countdown_time == 12):
            music_player.play_random_music()

        if self.countdown_time >= 0:
            self.update_image()
        else:
            self.timer.stop()
            QTimer.singleShot(1000, self.on_exit)
        
        self.countdown_time -= 1

    def update_image(self):
        """Loads and displays the appropriate countdown image, with alert effect in the last 3 seconds."""
        image_path = f"assets/images/{self.countdown_time}.tif"
        if os.path.exists(image_path):
            self.countdown_label.setPixmap(QPixmap(image_path))
        else:
            print(f"Warning: {image_path} not found.")  

    def resizeEvent(self, event):
        """Ensures the images resize with the window."""
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.countdown_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

    def launch_next_screen(self):
        """Transition to player entry screen after countdown."""
        import play_action_screen  
        self.next_screen = play_action_screen.PlayActionScreen()
        self.next_screen.showMaximized()
    
    def countdown_loop(self):
        self.show_logo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownWindow()
    window.show()
    sys.exit(app.exec())
