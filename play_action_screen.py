from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, Qt
import random
import threading
import time

class PlayActionScreen(QWidget):
    def __init__(self, red_players, green_players, photon_network, player_entry_screen_class, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")

        # Store players with their equipment IDs
        self.red_players = red_players
        self.green_players = green_players
        self.photon_network = photon_network
        self.player_entry_screen_class = player_entry_screen_class
        main_window = player_entry_screen_class

        # Main layout
        main_layout = QHBoxLayout()

        # Red team layout
        red_team_layout = QVBoxLayout()
        red_team_label = QLabel("RED TEAM")
        red_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        red_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        red_team_layout.addWidget(red_team_label)

        # Add Red Team players dynamically
        for player_id, player_name, equip_id in red_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center-align player info
            red_team_layout.addWidget(player_label)

        # Add Red Team layout to the main layout
        main_layout.addLayout(red_team_layout, stretch=1)

        # Current Game Action and Return Button layout (vertical)
        current_action_layout = QVBoxLayout()

        # Current Game Action label and text box
        current_action_label = QLabel("Current Game Action")
        current_action_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        current_action_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(current_action_label)

        self.current_action_text = QTextEdit()
        self.current_action_text.setReadOnly(True)
        self.current_action_text.setStyleSheet("background-color: black; color: lime; font-size: 16px;")
        self.current_action_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_action_layout.addWidget(self.current_action_text, stretch=1)

        # Return to Player Entry Screen button
        return_button = QPushButton("Return to Player Entry Screen")
        return_button.setStyleSheet("background-color: white; color: black;")
        return_button.clicked.connect(self.return_to_entry_screen)
        current_action_layout.addWidget(return_button)

        # Add Current Game Action and Button layout to the main layout
        main_layout.addLayout(current_action_layout, stretch=1)

        # Green team layout
        green_team_layout = QVBoxLayout()
        green_team_label = QLabel("GREEN TEAM")
        green_team_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        green_team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        green_team_layout.addWidget(green_team_label)

        # Add Green Team players dynamically
        for player_id, player_name, equip_id in green_players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Center-align player info
            green_team_layout.addWidget(player_label)

        # Add Green Team layout to the main layout
        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

        # Start traffic generator
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
                    equipment_code = f"{red_equip_id}:{green_equip_id}"
                else:
                    action_text = f"{green_player[1]} hit {red_player[1]}"
                    equipment_code = f"{green_equip_id}:{red_equip_id}"

                # Update the current game action with centered text using HTML
                centered_text = f"<div style='text-align: center;'>{action_text}</div>"
                self.append_to_current_action(centered_text)

                if self.photon_network:
                    self.photon_network.equipID(equipment_code)  # Broadcast equipment code to server
                else:
                    print(f"Skipping network broadcast: {equipment_code}")  # Debugging message # Broadcast equipment code to server

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_text = f"{red_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.append_to_current_action(centered_base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:43")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  # Debugging message
                elif counter == 20:
                    base_hit_text = f"{green_player[1]} hit the base!"
                    centered_base_hit_text = f"<div style='text-align: center;'>{base_hit_text}</div>"
                    self.append_to_current_action(centered_base_hit_text)
                    if self.photon_network:
                        self.photon_network.equipID(f"{red_equip_id}:53")  # Red team base hit
                    else:
                        print(f"Skipping network broadcast: {equipment_code}")  # Debugging message

                counter += 1
                time.sleep(random.randint(1, 3))  # Wait 1-3 seconds between messages

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text)  # Append text
        self.current_action_text.ensureCursorVisible()  # Ensure cursor is visible
        cursor = self.current_action_text.textCursor()  # Get cursor
        cursor.movePosition(cursor.MoveOperation.End)  # Move cursor to the end
        self.current_action_text.setTextCursor(cursor)  # Set cursor position

    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        from player_entry_screen import PlayerEntryScreen  # Import inside function to avoid circular import
        self._running = False  # Stop game thread
        self.close()  # Close the PlayActionScreen window
        global main_window 

        if self.photon_network is None:
            print("[DEBUG] Creating new PhotonNetwork instance")
            from client import PhotonNetwork  # Import inside function
            self.photon_network = PhotonNetwork(server_ip="127.0.0.1", server_port=7500, client_port=7501)

        # Create a new instance of PlayerEntryScreen
        print("[DEBUG] Reopening PlayerEntryScreen...")
        main_window = self.player_entry_screen_class(photon_network=self.photon_network)
        main_window.showMaximized()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    red_players = [("6005", "Scooby Deo Mt Opus", "111"), ("5000", "Euryum's Euryus Auxilus", "112")]
    green_players = [("6005", "Scooby Deo Mt Opus", "221"), ("5000", "Opus Mt Scooby Deo", "222")]
    screen = PlayActionScreen(red_players, green_players, None)
    screen.show()
    sys.exit(app.exec())
