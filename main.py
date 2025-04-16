from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
import sys
import signal
import socket

from ui.splash import SplashScreen
from ui.player_entry_screen import PlayerEntryScreen
from lib.play_action_screen import PlayActionScreen
from lib.countdown import CountdownWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.splash_screen = None
        self.player_entry_screen = None
        self.countdown_screen = None
        self.play_action_screen = None

        self.ip_address = None
        self.red_players = None
        self.green_players = None

    def open_splash(self):
        self.splash_screen = SplashScreen()
        self.splash_screen.showMaximized()
        QTimer.singleShot(3000, self.close_splash_and_open_entry)

    def close_splash_and_open_entry(self):
        if self.splash_screen:
            self.splash_screen.close()
            self.splash_screen.destroy()
            self.splash_screen = None

        self.open_entry()

    def open_entry(self):
        self.player_entry_screen = PlayerEntryScreen(on_exit=self.close_player_entry)
        self.player_entry_screen.showMaximized()

    def close_player_entry(self):
        if self.player_entry_screen:
            self.ip_address = self.player_entry_screen.network
            self.red_players, self.green_players = self.player_entry_screen.get_player_data()
            if self.red_players and self.green_players:
                self.player_entry_screen.close()
                self.player_entry_screen.destroy()
                self.player_entry_screen = None
                self.open_countdown()
            else:
                self.player_entry_screen.directions.setText("Error. Each team needs at least one player to run the program.")
                self.player_entry_screen.clear_game

    def open_countdown(self):
        self.countdown_screen = CountdownWindow(on_exit=self.close_countdown)
        self.countdown_screen.showMaximized()

    def close_countdown(self):
        if self.countdown_screen:
            self.countdown_screen.close()
            self.countdown_screen.destroy()
            self.countdown_screen = None
            self.open_play_action()

    def open_play_action(self):
        self.play_action_screen = PlayActionScreen(self.ip_address, self.red_players, self.green_players, on_exit=self.close_play_action)
        self.play_action_screen.showMaximized()

    def close_play_action(self):
        if self.play_action_screen:
            UDPTransmitSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            if(self.play_action_screen._running):
                for i in range(3):
                    UDPTransmitSocket.sendto(str.encode(str(221)), (self.ip_address, 7500))

            self.play_action_screen.close()
            self.play_action_screen.destroy()
            self.play_action_screen = None
            self.open_entry()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.open_splash()

    sys.exit(app.exec())
