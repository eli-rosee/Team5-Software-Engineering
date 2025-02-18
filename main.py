import sys
import signal
import splash
import player_entry_screen
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QMetaObject, Qt
from pynput import keyboard
import threading
import server  # Import the server module

main_window = None

def on_key_event(key):
    """ Global function to handle keyboard events """
    global main_window  

    try:
        if key == keyboard.Key.f3:
            print("Start game")
        elif key == keyboard.Key.f1:
            print("Back to loading screen")
        elif key == keyboard.Key.tab:
            #print("Tab pressed")
            QTimer.singleShot(0, main_window.change_tab_ind)  
        elif key == keyboard.Key.esc:
            QMetaObject.invokeMethod(main_window.timer, "stop", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(QApplication.instance(), "quit", Qt.ConnectionType.QueuedConnection)
        elif key == keyboard.Key.enter:
            QTimer.singleShot(0, main_window.add_player_by_key)
    except AttributeError:
        print("Error: Key press event encountered an issue")


def start_server_in_thread():
	""" Function to start the server in a separate thread """
	server.start_server(server_ip="0.0.0.0", server_port=7500, client_port=7501)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server_in_thread, daemon=True)

    server_thread.start()
    
    splash_window = splash.MainWindow()
    splash_window.show()

    transition_timer = QTimer()

    def transition_to_player_entry():
        global main_window  

        transition_timer.stop()
        splash_window.close()

        main_window = player_entry_screen.PlayerEntryScreen()
        main_window.showMaximized()

        QMetaObject.invokeMethod(
            main_window.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection
        )

        listener = keyboard.Listener(on_press=on_key_event)
        listener.start()

    transition_timer.timeout.connect(transition_to_player_entry)
    transition_timer.start(15000)  

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())
