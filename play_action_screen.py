from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
import sys
import random
import threading
import time

class PlayActionScreen(QWidget):
    action_signal = pyqtSignal(str)
    score_signal = pyqtSignal(str, str)  
    team_score_signal = pyqtSignal(str)

    def __init__(self, red_players, green_players, photon_network, player_entry_screen_instance, parent=None):
        super().__init__(parent)
        self.action_signal.connect(self.append_to_current_action)
        self.score_signal.connect(self.change_player_score)
        self.team_score_signal.connect(self.change_team_score)
        self.red_player_scores = {player_id: 0 for player_id, _, _ in red_players}
        self.green_player_scores = {player_id: 0 for player_id, _, _ in green_players}
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.flash_high_team_score)
        self.flash_state = True
        self.flash_timer.start(500)
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")
        

        # Store players with their equipment IDs
        self.red_players = red_players
        self.green_players = green_players
        self.photon_network = photon_network
        self.player_entry_screen = player_entry_screen_instance 

        self.red_player_labels = {}
        self.green_player_labels = {}

        main_layout = QHBoxLayout()

        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_score = QLabel("0")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_score.setStyleSheet("font-size: 50px; font-weight: bold; color: red;")
        red_team_score.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_layout.addWidget(red_team_label)
        red_team_layout.addWidget(red_team_score)

        self.red_team_score_label = red_team_score
        self.red_team_score = 0

        self.red_player_layout = QVBoxLayout()
        red_players_count = len(red_players)
        for i, (player_id, player_name, equip_id) in enumerate(red_players):
            score = 0

            if i < red_players_count - 1 or i == 0:
               self.red_player_layout.addStretch(1)
    
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id}) Score: {score}")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.red_player_layout.addWidget(player_label)

            self.red_player_labels[f'{player_id}'] = player_label

        red_team_layout.addLayout(self.red_player_layout)

        red_team_layout.addStretch()

        main_layout.addLayout(red_team_layout)
        self.setLayout(main_layout)

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

        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_score = QLabel("0")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_score.setStyleSheet("font-size: 50px; font-weight: bold; color: green;")
        green_team_score.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_layout.addWidget(green_team_label)
        green_team_layout.addWidget(green_team_score)

        self.green_team_score_label = green_team_score
        self.green_team_score = 0

        self.green_player_layout = QVBoxLayout()
        green_players_count = len(green_players)
        for i, (player_id, player_name, equip_id) in enumerate(green_players):
            score = 0

            if i < green_players_count - 1 or i == 0:
               self.green_player_layout.addStretch(1)
    
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id}) Score: {score}")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.green_player_layout.addWidget(player_label)

            self.green_player_labels[f'{player_id}'] = player_label

        green_team_layout.addLayout(self.green_player_layout)

        green_team_layout.addStretch()

        main_layout.addLayout(green_team_layout)
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
                    equip_parts = equipment_code.split(":")
                    if len(equip_parts) == 2:
                        attacker_id, target_id = equip_parts
                        self.score_signal.emit(attacker_id, target_id)
                else:
                    action_text = f"{green_player[1]} hit {red_player[1]}"
                    equipment_code = f"{green_equip_id}:{red_equip_id}"
                    equip_parts = equipment_code.split(":")
                    if len(equip_parts) == 2:
                        attacker_id, target_id = equip_parts
                        self.score_signal.emit(attacker_id, target_id)

                centered_text = f"<div style='text-align: center;'>{action_text}</div>"
                self.action_signal.emit(centered_text)


                if self.photon_network:
                    self.photon_network.equipID(equipment_code)  # Broadcast equipment code to server
                else:
                    print(f"Skipping network broadcast: {equipment_code}")  

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_text = f"{red_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.action_signal.emit(centered_base_hit_text)
                    self.team_score_signal.emit(base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:43")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  
                elif counter == 20:
                    base_hit_text = f"{green_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.action_signal.emit(centered_base_hit_text)
                    self.team_score_signal.emit(base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:53")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  

                counter += 1
                time.sleep(random.randint(1, 3))  

    def closeEvent(self, event):
        from music import music_player
        music_player.stop_music()
        event.accept()

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text) 
        self.current_action_text.ensureCursorVisible()  
        cursor = self.current_action_text.textCursor()  
        cursor.movePosition(cursor.MoveOperation.End)  
        self.current_action_text.setTextCursor(cursor)  

    def change_team_score(self, text):
        player_name = text.split(" hit")[0].strip()

        red_names = [name for _, name, _ in self.red_players]
        green_names = [name for _, name, _ in self.green_players]

        if player_name in red_names:
            self.red_team_score += 100
            self.red_team_score_label.setText(str(self.red_team_score))
            print(f"Updated Red Team Score: {self.red_team_score}")

            for player_id, name, equip_id in self.red_players:
                if name == player_name:
                    self.red_player_scores[player_id] += 100
                    label = self.red_player_labels.get(player_id)
                    if label:
                        label.setText(f"{player_id} - {name} (Equipment: {equip_id}) Score: {self.red_player_scores[player_id]}")
                    break

        elif player_name in green_names:
            self.green_team_score += 100
            self.green_team_score_label.setText(str(self.green_team_score))
            print(f"Updated Green Team Score: {self.green_team_score}")

            # Award 100 points to individual player
            for player_id, name, equip_id in self.green_players:
                if name == player_name:
                    self.green_player_scores[player_id] += 100
                    label = self.green_player_labels.get(player_id)
                    if label:
                        label.setText(f"{player_id} - {name} (Equipment: {equip_id}) Score: {self.green_player_scores[player_id]}")
                    break
        else:
            print("ERROR: Player not found in either team.")

        self.sort_players()

               

    def change_player_score(self, attacker_equip_id, target_equip_id):
        attacker = None
        target = None
        attacker_team = None
        target_team = None

        for player in self.red_players:
            if player[2] == attacker_equip_id:
                attacker = player
                attacker_team = "red"
        for player in self.green_players:
            if player[2] == attacker_equip_id:
                attacker = player
                attacker_team = "green"
        for player in self.red_players + self.green_players:
            if player[2] == target_equip_id:
                target = player
                target_team = "red" if player in self.red_players else "green"

        if not attacker:
            print(f"Unknown attacker with equip ID {attacker_equip_id}")
            return

        if target_equip_id in ("43", "53"):
            score = 100
            label_dict = self.red_player_labels if attacker_team == "red" else self.green_player_labels
            score_dict = self.red_player_scores if attacker_team == "red" else self.green_player_scores

            player_id = attacker[0]
            name = attacker[1]
            label = label_dict.get(player_id)

            if label:
                if not name.startswith("🅱"):
                    name = f"🅱 {name}"
                score_dict[player_id] += score
                label.setText(f"{player_id} - {name} (Equipment: {attacker[2]}) Score: {score_dict[player_id]}")
            return

        if attacker_team and target_team:
            label_dict = self.red_player_labels if attacker_team == "red" else self.green_player_labels
            score_dict = self.red_player_scores if attacker_team == "red" else self.green_player_scores

            player_id = attacker[0]
            name = attacker[1]
            label = label_dict.get(player_id)

            if attacker_team == target_team:
                score_change = -10  
            else:
                score_change = 10   

            score_dict[player_id] += score_change

            self.sort_players()

            if label:
                label.setText(f"{player_id} - {name} (Equipment: {attacker[2]}) Score: {score_dict[player_id]}")

            if attacker_team == "red":
                self.red_team_score += score_change
                self.red_team_score_label.setText(str(self.red_team_score))
                print(f"Updated Red Team Score: {self.red_team_score}")
            else:
                self.green_team_score += score_change
                self.green_team_score_label.setText(str(self.green_team_score))
                print(f"Updated Green Team Score: {self.green_team_score}")

    def sort_players(self):
        red_sorted = sorted(self.red_players, key=lambda p: self.red_player_scores.get(p[0], 0), reverse=True)
        for i in reversed(range(self.red_player_layout.count())):
            widget = self.red_player_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for player_id, _, _ in red_sorted:
            self.red_player_layout.addWidget(self.red_player_labels[player_id])
        self.red_player_layout.addStretch()

        green_sorted = sorted(self.green_players, key=lambda p: self.green_player_scores.get(p[0], 0), reverse=True)
        for i in reversed(range(self.green_player_layout.count())):
            widget = self.green_player_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for player_id, _, _ in green_sorted:
            self.green_player_layout.addWidget(self.green_player_labels[player_id])
        self.green_player_layout.addStretch()

    def flash_high_team_score(self):
        if self.red_team_score > self.green_team_score:
            self.red_team_score_label.setStyleSheet(
                f"font-size: 50px; font-weight: bold; color: {'red' if self.flash_state else 'black'};"
            )
            self.green_team_score_label.setStyleSheet("font-size: 50px; font-weight: bold; color: green;")
        elif self.green_team_score > self.red_team_score:
            self.green_team_score_label.setStyleSheet(
                f"font-size: 50px; font-weight: bold; color: {'green' if self.flash_state else 'black'};"
            )
            self.red_team_score_label.setStyleSheet("font-size: 50px; font-weight: bold; color: red;")
        else:
            # Tie: both show normally
            self.red_team_score_label.setStyleSheet("font-size: 50px; font-weight: bold; color: red;")
            self.green_team_score_label.setStyleSheet("font-size: 50px; font-weight: bold; color: green;")
        
        self.flash_state = not self.flash_state



    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        from player_entry_screen import PlayerEntryScreen  
        self._running = False
        self.game_timer.stop()  # Stop the game timer

        if self.photon_network:
            self.photon_network.send_stop_signal()

        self.close()  

        self.player_entry_screen.showMaximized() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    red_players = [("6005", "Player 1", "111"), ("5000", "Player 2", "112")]
    green_players = [("6005", "Player 3", "221"), ("5000", "Player 4", "222")]
    screen = PlayActionScreen(red_players, green_players, None, None)
    screen.show()
    sys.exit(app.exec())
