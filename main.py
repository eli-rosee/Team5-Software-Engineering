import sys
import signal
import splash
import player_entry_screen
import countdown
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QMetaObject, Qt
from pynput import keyboard
import threading
import server  # Import the server module

main_window = None
countdown_window = None
splash_window = None
player_entry_screen_window = None  

def on_key_event(key):
    """ Global function to handle keyboard events """
    global main_window, countdown_window, player_entry_screen_window

    try:
        if key == keyboard.Key.f3:
            print("Start game")
        elif key == keyboard.Key.f1:
            print("Back to loading screen")
        elif key == keyboard.Key.f12:
                QTimer.singleShot(0, main_window.clear_all_players)
        elif key == keyboard.Key.tab:
            if main_window is not None:
                QTimer.singleShot(0, main_window.change_tab_ind)
            else:
                print("Main window not initialized yet.")
        elif key == keyboard.Key.f5:
            if splash_window:
                splash_window.close()
            else:
                print("Splash window is already closed or not initialized.")
            
            if player_entry_screen_window is not None and player_entry_screen_window.isVisible():
                print("Closing Player Entry Screen...")
                QMetaObject.invokeMethod(player_entry_screen_window, "close", Qt.ConnectionType.QueuedConnection)

            else:
                print("Splash window is already closed or not initialized.")

            if countdown_window is None or not countdown_window.isVisible():
                countdown_window = countdown.MainWindow()
                countdown_window.showMaximized()
                QTimer.singleShot(0, main_window.transition_to_play_action_screen)
                print("Countdown window should now be visible")
            else:
                print("Countdown window is already open.")
        elif key == keyboard.Key.esc:
            if main_window and hasattr(main_window, 'timer'):
                QMetaObject.invokeMethod(main_window.timer, "stop", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(QApplication.instance(), "quit", Qt.ConnectionType.QueuedConnection)
        elif key == keyboard.Key.enter:
            if main_window is not None:
                QTimer.singleShot(0, main_window.add_player_by_key)
            else:
                print("Main window not initialized yet.")
    except AttributeError as e:
        print(f"Error: Key press event encountered an issue: {e}")

def start_server_in_thread():
    """ Function to start the server in a separate thread """
    try:
        server.start_server(server_ip="0.0.0.0", server_port=7500, client_port=7501)
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    server_thread = threading.Thread(target=start_server_in_thread, daemon=True)
    server_thread.start()

    print("Starting Splash Screen...")

    try:
        splash_window = splash.MainWindow()
        splash_window.show()
    except Exception as e:
        print(f"Error initializing splash screen: {e}")
        sys.exit(1) 

    transition_timer = QTimer()

    def transition_to_player_entry():
        global main_window, player_entry_screen_window

        print("Transitioning to Player Entry Screen...")

        transition_timer.stop()
        
        if splash_window:
            splash_window.close()

        try:
            player_entry_screen_window = player_entry_screen.PlayerEntryScreen() 
            main_window = player_entry_screen_window  
            main_window.showMaximized()
            QMetaObject.invokeMethod(
                main_window.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection
            )
        except Exception as e:
            print(f"Error initializing Player Entry Screen: {e}")
            sys.exit(1)  # Exit if main window fails

        # Start keyboard listener
        listener = keyboard.Listener(on_press=on_key_event)
        listener.start()

    transition_timer.timeout.connect(transition_to_player_entry)
    transition_timer.start(3000)  # 15 seconds

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())
