from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, Qt
import random
import threading
import time

class PlayActionScreen(QWidget):
    def __init__(self, red_players, green_players, photon_network, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Action Screen")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black; color: white;")

        # Store players with their equipment IDs
        self.red_players = red_players  # List of tuples: (player_id, player_name, equip_id)
        self.green_players = green_players  # List of tuples: (player_id, player_name, equip_id)
        self.photon_network = photon_network  # Store the PhotonNetwork instance

        # Main layout
        main_layout = QVBoxLayout()

        # Teams layout (Red Team | Green Team)
        teams_layout = QHBoxLayout()

        # Red team
        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        red_team_layout.addWidget(red_team_label)

        # Add Red Team players dynamically
        for player_id, player_name, equip_id in red_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            red_team_layout.addWidget(player_label)

        teams_layout.addLayout(red_team_layout)

        # Green team
        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        green_team_layout.addWidget(green_team_label)

        # Add Green Team players dynamically
        for player_id, player_name, equip_id in green_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            green_team_layout.addWidget(player_label)

        teams_layout.addLayout(green_team_layout)

        # Add teams layout to main layout with stretch factor 3 (75% of the screen)
        main_layout.addLayout(teams_layout, stretch=3)

        # Current Game Action
        current_action_label = QLabel("Current Game Action")
        current_action_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        current_action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(current_action_label)

        self.current_action_text = QTextEdit()
        self.current_action_text.setReadOnly(True)
        self.current_action_text.setStyleSheet("background-color: white; color: black;")
        
        # Add current game action box with stretch factor 1 (25% of the screen)
        main_layout.addWidget(self.current_action_text, stretch=1)

        # Button to return to player entry screen
        return_button = QPushButton("Return to Player Entry Screen")
        return_button.setStyleSheet("background-color: white; color: black;")
        return_button.clicked.connect(self.return_to_entry_screen)
        main_layout.addWidget(return_button)

        self.setLayout(main_layout)

        # Start the traffic generator
        self._running = True
        self.traffic_thread = threading.Thread(target=self.generate_traffic, daemon=True)
        self.traffic_thread.start()

    def generate_traffic(self):
        """Simulate game traffic and update the current game action."""
        counter = 0
        while self._running:
            if len(self.red_players) >= 1 and len(self.green_players) >= 1:  # Ensure there are players
                # Randomly select a red and green player
                red_player = random.choice(self.red_players)
                green_player = random.choice(self.green_players)

                # Extract equipment IDs
                red_equip_id = red_player[2]  # Equipment ID is at index 2
                green_equip_id = green_player[2]  # Equipment ID is at index 2

                # Simulate interactions between players
                if random.randint(1, 2) == 1:
                    action_text = f"{red_player[1]} hit {green_player[1]}"
                    equipment_code = f"{red_equip_id}:{green_equip_id}"  # Format: 111:222
                else:
                    action_text = f"{green_player[1]} hit {red_player[1]}"
                    equipment_code = f"{green_equip_id}:{red_equip_id}"  # Format: 222:111

                # Update the current game action
                self.current_action_text.append(action_text)

                # Broadcast the equipment code to the server
                self.photon_network.equipID(equipment_code)  # Send the equipment code

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_text = f"{red_player[1]} hit the base!"
                    self.current_action_text.append(base_hit_text)
                    self.photon_network.equipID(f"{red_equip_id}:43")  # Red team base hit
                elif counter == 20:
                    base_hit_text = f"{green_player[1]} hit the base!"
                    self.current_action_text.append(base_hit_text)
                    self.photon_network.equipID(f"{green_equip_id}:53")  # Green team base hit

                counter += 1
                time.sleep(random.randint(1, 3))  # Wait 1-3 seconds between messages

    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        self._running = False  # Stop traffic generator thread
        self.close()  # Close PlayActionScreen window

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    red_players = [("6005", "Scooby Deo Mt Opus"), ("5000", "Euryum's Euryus Auxilus")]
    green_players = [("6005", "Scooby Deo Mt Opus"), ("5000", "Opus Mt Scooby Deo")]
    screen = PlayActionScreen(red_players, green_players)
    screen.show()
    sys.exit(app.exec())
