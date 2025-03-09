from PyQt6.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
import sys
import os

class CountdownWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: black;")

        # Background label (for `background.tif`)
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Countdown image label
        self.countdown_label = QLabel(self)
        self.countdown_label.setScaledContents(True)
        self.countdown_label.setGeometry(0, 0, self.width(), self.height())

        self.showMaximized()  # Fullscreen mode

         #Show the logo first
        self.show_logo()

    def force_close(self):
        """Closes the countdown window and exits the application."""
        print("DEBUG: Closing Countdown Window...")
        self.close()
        QApplication.quit()

    def show_logo(self):
        """Displays the logo before the countdown starts."""
        logo_path = "graphics/countdown_images/30.tif"
        if os.path.exists(logo_path):
            self.countdown_label.setPixmap(QPixmap(logo_path))
        else:
            print("Warning: Logo not found.")

        # Show logo for 3 seconds, then start countdown
        QTimer.singleShot(3000, self.setup_background)

    def setup_background(self):
        """Sets the background image before starting the countdown."""
        background_path = "graphics/countdown_images/30.tif"
        if os.path.exists(background_path):
            self.background_label.setPixmap(QPixmap(background_path))
        else:
            print("Warning: Background image not found.")

        # Start the countdown
        self.start_countdown()

    def start_countdown(self):
        """Starts the countdown timer and updates images every second."""
        self.countdown_time = 30  # Start countdown from 30 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.update_image()
        self.timer.start(1000)  # Update every second

    def update_countdown(self):
        """Updates the countdown image every second."""
        self.countdown_time -= 1

        if self.countdown_time >= 0:
            self.update_image()
        else:
            self.timer.stop()
            self.show_final_image()  # Show the final "0" image before transitioning

    def update_image(self):
        """Loads and displays the appropriate countdown image, with alert effect in the last 3 seconds."""
        if self.countdown_time <= 3:  # Show alert-on.tif when reaching last 3 seconds
            alert_path = "graphics/alert-on.tif"
            if os.path.exists(alert_path):
                self.background_label.setPixmap(QPixmap(alert_path))
            else:
                print("Warning: Alert image not found.")

        # Update countdown number
        image_path = f"graphics/countdown_images/{self.countdown_time}.tif"
        if os.path.exists(image_path):
            self.countdown_label.setPixmap(QPixmap(image_path))
        else:
            print(f"Warning: {image_path} not found.")  # Fallback warning if images are missing

    def show_final_image(self):
        """Displays the final 'countdown_0.tif' before transitioning."""
        final_image_path = "graphics/countdown_images/countdown_0.tif"
        if os.path.exists(final_image_path):
            self.countdown_label.setPixmap(QPixmap(final_image_path))
        else:
            print("Warning: Final countdown image not found.")

        # Hold final image for 1 second before transitioning
        QTimer.singleShot(1000, self.force_close)
        #QTimer.singleShot(1000, self.launch_next_screen)

    def resizeEvent(self, event):
        """Ensures the images resize with the window."""
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.countdown_label.setGeometry(0, 0, self.width(), self.height())
        event.accept()

    def launch_next_screen(self):
        """Transition to player entry screen after countdown."""
        import play_action_screen  # Import here to avoid circular imports
        self.next_screen = play_action_screen.PlayActionScreen()
        self.next_screen.showMaximized()
        self.close()  # Close countdown window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownWindow()
    window.show()
    sys.exit(app.exec())
