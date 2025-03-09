from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
import random
import threading
import time

class PlayActionScreen(QWidget):
    def __init__(self, red_players, green_players, photon_network, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Action Screen")
        self.showMaximized()
        self.setStyleSheet("background-color: black; color: white;")

        self.red_players = red_players
        self.green_players = green_players
        self.photon_network = photon_network
        self._running = True

        self.init_ui()
        self.start_traffic_generator()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QHBoxLayout()

        # Red team layout
        red_team_layout = self.create_team_layout("RED TEAM", "red", self.red_players)
        main_layout.addLayout(red_team_layout, stretch=1)

        # Current action and return button layout
        current_action_layout = self.create_current_action_layout()
        main_layout.addLayout(current_action_layout, stretch=1)

        # Green team layout
        green_team_layout = self.create_team_layout("GREEN TEAM", "green", self.green_players)
        main_layout.addLayout(green_team_layout, stretch=1)

        self.setLayout(main_layout)

    def create_team_layout(self, team_name, color, players):
        """Create a layout for a team."""
        team_layout = QVBoxLayout()
        team_label = QLabel(team_name)
        team_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        team_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        team_layout.addWidget(team_label)

        for player_id, player_name, equip_id in players:
            player_label = QLabel(f"{player_id} - {player_name} (Equipment: {equip_id})")
            player_label.setStyleSheet("font-size: 16px; color: white;")
            player_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            team_layout.addWidget(player_label)

        return team_layout

    def create_current_action_layout(self):
        """Create the layout for current game action and return button."""
        current_action_layout = QVBoxLayout()

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

        return current_action_layout

    def start_traffic_generator(self):
        """Start the traffic generator thread."""
        self.traffic_thread = threading.Thread(target=self.generate_traffic, daemon=True)
        self.traffic_thread.start()

    def generate_traffic(self):
        """Simulate game traffic and update the current game action."""
        counter = 0
        while self._running and self.red_players and self.green_players:
            red_player = random.choice(self.red_players)
            green_player = random.choice(self.green_players)

            if random.randint(1, 2) == 1:
                action_text = f"{red_player[1]} hit {green_player[1]}"
                equipment_code = f"{red_player[2]}:{green_player[2]}"
            else:
                action_text = f"{green_player[1]} hit {red_player[1]}"
                equipment_code = f"{green_player[2]}:{red_player[2]}"

            self.append_to_current_action(f"<div style='text-align: center;'>{action_text}</div>")
            self.photon_network.equipID(equipment_code)

            if counter == 10:
                self.append_to_current_action(f"<div style='text-align: center;'>{red_player[1]} hit the base!</div>")
                self.photon_network.equipID(f"{red_player[2]}:43")
            elif counter == 20:
                self.append_to_current_action(f"<div style='text-align: center;'>{green_player[1]} hit the base!</div>")
                self.photon_network.equipID(f"{green_player[2]}:53")

            counter += 1
            time.sleep(random.randint(1, 3))

    def append_to_current_action(self, text):
        """Append text to the current action box and ensure it scrolls down."""
        self.current_action_text.append(text)
        self.current_action_text.ensureCursorVisible()

    def return_to_entry_screen(self):
        """Stop the traffic generator and return to the player entry screen."""
        self._running = False
        self.close()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    red_players = [("6005", "Scooby Deo Mt Opus", "111"), ("5000", "Euryum's Euryus Auxilus", "112")]
    green_players = [("6005", "Scooby Deo Mt Opus", "221"), ("5000", "Opus Mt Scooby Deo", "222")]
    screen = PlayActionScreen(red_players, green_players, None)
    screen.show()
    sys.exit(app.exec())
