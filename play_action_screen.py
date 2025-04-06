from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, Qt
import random
import threading
import time
from playsound import playsound
import pygame
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


class PlayActionScreen(QWidget):
    def __init__(self, red_players, green_players, photon_network, player_entry_screen_instance, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")
        global music_player
        music_player = MusicPlayer()
        music_player.play_random_music()
    

        # Store players with their equipment IDs
        self.red_players = red_players
        self.green_players = green_players
        self.photon_network = photon_network
        self.player_entry_screen = player_entry_screen_instance 

        main_layout = QHBoxLayout()

        # Red team layout
        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_layout.addWidget(red_team_label)

        # Add Red Team players
        for player_id, player_name, equip_id in red_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  
            red_team_layout.addWidget(player_label)

        main_layout.addLayout(red_team_layout, stretch=1)

        current_action_layout = QVBoxLayout()

        # Game timer display
        self.game_timer_label = QLabel("06:00")
        self.game_timer_label.setStyleSheet("font-size: 40px; font-weight: bold; color: yellow;")
        self.game_timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(self.game_timer_label)

        current_action_label = QLabel("Current Game Action")
        current_action_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        current_action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(current_action_label)

        self.current_action_text = QTextEdit()
        self.current_action_text.setReadOnly(True)
        self.current_action_text.setStyleSheet("background-color: black; color: lime; font-size: 16px;")
        self.current_action_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(self.current_action_text, stretch=1)

        return_button = QPushButton("Return to Player Entry Screen")
        return_button.setStyleSheet("background-color: white; color: black;")
        return_button.clicked.connect(self.return_to_entry_screen)
        current_action_layout.addWidget(return_button)

        main_layout.addLayout(current_action_layout, stretch=1)

        # Green team layout
        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_layout.addWidget(green_team_label)

        # Add Green Team players 
        for player_id, player_name, equip_id in green_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  
            green_team_layout.addWidget(player_label)

        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

        # Initialize and start game timer (6 minutes)
        self.game_time_remaining = 6 * 60  # 6 minutes in seconds
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_timer)
        self.game_timer.start(1000)  # Update every second

        # Start traffic generator
        self._running = True
        self.traffic_thread = threading.Thread(target=self.generate_traffic, daemon=True)
        self.traffic_thread.start()

    def update_game_timer(self):
        """Update the game timer display every second."""
        self.game_time_remaining -= 1
        
        if self.game_time_remaining <= 0:
            self.game_timer.stop()
            self.game_timer_label.setText("00:00")
            self.append_to_current_action("<div style='text-align: center; color: red;'>GAME OVER!</div>")
            # Stop traffic generator
            self._running = False
            # Return to player entry screen after brief delay
            QTimer.singleShot(2000, self.return_to_entry_screen)
        else:
            minutes = self.game_time_remaining // 60
            seconds = self.game_time_remaining % 60
            self.game_timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def generate_traffic(self):
        """Simulate game traffic and update the current game action."""
        counter = 0
        while self._running and self.game_time_remaining > 0:  # Stop traffic when game ends
            if len(self.red_players) >= 1 and len(self.green_players) >= 1:  
                red_player = random.choice(self.red_players)
                green_player = random.choice(self.green_players)

                red_equip_id = red_player[2] 
                green_equip_id = green_player[2]  

                # Simulate interactions between players
                if random.randint(1, 2) == 1:
                    action_text = f"{red_player[1]} hit {green_player[1]}"
                    equipment_code = f"{red_equip_id}:{green_equip_id}"
                else:
                    action_text = f"{green_player[1]} hit {red_player[1]}"
                    equipment_code = f"{green_equip_id}:{red_equip_id}"

                centered_text = f"<div style='text-align: center;'>{action_text}</div>"
                self.append_to_current_action(centered_text)

                if self.photon_network:
                    self.photon_network.equipID(equipment_code)  # Broadcast equipment code to server
                else:
                    print(f"Skipping network broadcast: {equipment_code}")  

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_text = f"{red_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.append_to_current_action(centered_base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:43")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  
                elif counter == 20:
                    base_hit_text = f"{green_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.append_to_current_action(centered_base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:53")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  

                counter += 1
                time.sleep(random.randint(1, 3))  

    def closeEvent(self, event):
        global music_player
        music_player = MusicPlayer()
        music_player.play_random_music()
        event.accept()

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text) 
        self.current_action_text.ensureCursorVisible()  
        cursor = self.current_action_text.textCursor()  
        cursor.movePosition(cursor.MoveOperation.End)  
        self.current_action_text.setTextCursor(cursor)  

    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        from player_entry_screen import PlayerEntryScreen  
        self._running = False
        self.game_timer.stop()  # Stop the game timer
        self.close()  

        self.player_entry_screen.showMaximized() 


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    red_players = [("6005", "Scooby Deo Mt Opus", "111"), ("5000", "Euryum's Euryus Auxilus", "112")]
    green_players = [("6005", "Scooby Deo Mt Opus", "221"), ("5000", "Opus Mt Scooby Deo", "222")]
    screen = PlayActionScreen(red_players, green_players, None)
    screen.show()
    sys.exit(app.exec())
