import sys
import signal
import splash
import player_entry_screen

if __name__ == "__main__":
    app = splash.QApplication(sys.argv)

    # Initialize splash screen
    splash_window = splash.MainWindow()
    splash_window.show()

    # Function to transition to player entry screen
    def transition_to_player_entry():
        splash_window.close()

        # Initialize player entry screen
        main_window = player_entry_screen.PlayerEntryScreen()
        main_window.showMaximized()

        # Capture keyboard events
        player_entry_screen.QMetaObject.invokeMethod(main_window.red_row[0][3], "setFocus", player_entry_screen.Qt.ConnectionType.QueuedConnection)

    listener = player_entry_screen.keyboard.Listener(player_entry_screen.on_key_event)
    listener.start()

    # Start timer to transition after 3 seconds
    transition_timer = player_entry_screen.QTimer()
    transition_timer.timeout.connect(transition_to_player_entry)
    transition_timer.start(3000)

    # Handle SIGINT (Ctrl+C) for safe termination
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())