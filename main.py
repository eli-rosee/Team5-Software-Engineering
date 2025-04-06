import sys
import signal
import splash
import player_entry_screen
import countdown
import play_action_screen
import time
import random
import pygame
from playsound import playsound
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QMetaObject, Qt, QObject, pyqtSlot
from pynput import keyboard
import threading
import server 

main_window = None
countdown_window = None
splash_window = None
player_entry_screen_window = None  
play_action_screen_window = None
global play_action_handler
music_player = None

class MusicPlayer:
    def __init__(self):
        self.tracks = [
            "music/Track01.mp3",
            "music/Track02.mp3",
            "music/Track03.mp3",
            "music/Track04.mp3",
            "music/Track05.mp3",
            "music/Track06.mp3",
            "music/Track07.mp3",
            "music/Track08.mp3"
        ]
        self.playing = False
        pygame.mixer.init()

    def play_random_music(self):
        def play_loop():
            self.playing = True
            while self.playing:
                track = random.choice(self.tracks)
                print(f"Now playing: {track}")
                pygame.mixer.music.load(track)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if not self.playing:
                        pygame.mixer.music.stop()
                        break
                    time.sleep(0.1)

        threading.Thread(target=play_loop, daemon=True).start()

    def stop_music(self):
        self.playing = False
        pygame.mixer.music.stop()
        print("Music stopped.")

class CountdownHandler(QObject):
    @pyqtSlot() 
    def open_countdown_window(self):
        global countdown_window

        if countdown_window is None or not countdown_window.isVisible():
            countdown_window = countdown.CountdownWindow()
            countdown_window.showMaximized()
        else:
            print("DEBUG: Countdown window is already open.")

class PlayActionHandler(QObject):
    @pyqtSlot() 
    def open_play_action(self):
        global play_action_screen_window  

        if play_action_screen_window is None or not play_action_screen_window.isVisible():
            from player_entry_screen import PlayerEntryScreen 
            red_players, green_players = player_entry_screen_window.get_player_data()
            play_action_screen_window = play_action_screen.PlayActionScreen(
                red_players=red_players,
                green_players=green_players,
                photon_network=player_entry_screen_window.photon_network,  
                player_entry_screen_instance=player_entry_screen_window  
            )   
            play_action_screen_window.showMaximized()

        else:
            print("DEBUG: PlayActionScreen is already open.")



def on_key_event(key):
    """ Global function to handle keyboard events """
    global main_window, countdown_window, player_entry_screen_window, play_action_screen_window

    try:
        if key == keyboard.Key.f3:
            print("Nothing")
        elif key == keyboard.Key.f1:
            print("Nothing")
        elif key == keyboard.Key.tab:
            if main_window is not None:
                QTimer.singleShot(0, main_window.change_tab_ind)
            else:
                print("Main window not initialized yet.")
        elif key == keyboard.Key.f12:
                QTimer.singleShot(0, main_window.clear_all_players)
        elif key == keyboard.Key.f5:
            red_players, green_players = player_entry_screen_window.get_player_data()
            missing_data = False

            for row in player_entry_screen_window.red_row + player_entry_screen_window.green_row:  
                player_id = row[3].text().strip()
                code_name = row[4].text().strip()
                equip_id = row[5].text().strip()

                if player_id and (not code_name or not equip_id):  
                    missing_data = True  
                    break  

            if not red_players or not green_players:
                player_entry_screen_window.directions.setText("There is an empty team")
            elif missing_data:
                player_entry_screen_window.directions.setText("Please fill in all equipment IDs and codenames before starting the game")
            else:
                if splash_window:
                    splash_window.close()
                else:
                    print("Splash window is already closed or not initialized.")
                
                if player_entry_screen_window is not None and player_entry_screen_window.isVisible():
                    QMetaObject.invokeMethod(player_entry_screen_window, "close", Qt.ConnectionType.QueuedConnection)
                else:
                    print("Splash window is already closed or not initialized.")

                QMetaObject.invokeMethod(countdown_handler, "open_countdown_window", Qt.ConnectionType.QueuedConnection) 
                time.sleep(30)
                QMetaObject.invokeMethod(play_action_handler, "open_play_action", Qt.ConnectionType.QueuedConnection)
                music_player.play_random_music()
                player_entry_screen_window.photon_network.send_start_signal()

        elif key == keyboard.Key.esc:
            if main_window and hasattr(main_window, 'timer'):
                QMetaObject.invokeMethod(main_window.timer, "stop", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(QApplication.instance(), "quit", Qt.ConnectionType.QueuedConnection)
        elif key == keyboard.Key.enter:
            main_window = player_entry_screen_window
            if main_window is not None:
                QTimer.singleShot(0, main_window.add_player_by_key)
            else:
                print("ERROR: Main window is None. Cannot add player.")
            
    except AttributeError as e:
        print(f"Error: Key press event encountered an issue: {e}")

def start_server_in_thread():
    """ Function to start the server in a separate thread """
    try:
        server.server_instance.start_server()
        #server.start_server(server_ip="127.0.0.1", server_port=7500, client_port=7501)
    except Exception as e:
        print(f"Error starting server: {e}")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    countdown_handler = CountdownHandler()
    play_action_handler = PlayActionHandler()
    listener = keyboard.Listener(on_press=on_key_event)
    listener.start()

    server_thread = threading.Thread(target=start_server_in_thread, daemon=True)
    server_thread.start()

    music_player = MusicPlayer()


    try:
        splash_window = splash.MainWindow()
        splash_window.show()
    except Exception as e:
        print(f"Error initializing splash screen: {e}")
        sys.exit(1) 

    transition_timer = QTimer()

    def transition_to_player_entry():
        global main_window, player_entry_screen_window
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
            sys.exit(1)  


    transition_timer.timeout.connect(transition_to_player_entry)
    transition_timer.start(3000)  

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec())
