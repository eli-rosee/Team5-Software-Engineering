from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QSizePolicy, QLabel, QLineEdit, QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
import sys
import ipaddress
import socket

sys.path.insert(1, 'lib/')
import database

class PlayerEntryScreen(QWidget):
    
    def __init__(self, on_exit):

        # IP ADDRESS (Can be changed)
        self.network = "127.0.0.1"
        self.broadcast_port = 7500
        self.broadcast = (self.network, self.broadcast_port)
        self.UDPBroadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        self.start_game = on_exit

        # Declare and initiate some basic attributes of the Player Entry Screen Window
        super().__init__()
        self.setWindowTitle("Player Entry Screen")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.popup_active = False 
        main_layout = QVBoxLayout()
        QApplication.setStyle("windows")
        self.tab_ind = 0
        self.team_red = True
        self.db = database.Database()
        
        # Large amount of nonfunctional UI code
        self.title_label = QLabel("Player Entry Screen")
        self.directions = QLabel("Enter a NEW PLAYER ID:")
        
        self.directions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.directions.setStyleSheet("background-color: black; color: white; height: 10px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: blue;")

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.directions)
        
        teams_layout = QHBoxLayout()
        self.red_team_layout = QVBoxLayout()

        self.red_team_title = QLabel("RED TEAM")
        self.red_team_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_team_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.red_team_layout.addWidget(self.red_team_title)

        self.red_team_info_layout = QHBoxLayout()

        self.add_label = QLabel("")
        self.add_label.setFixedWidth(37)
        self.add_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.add_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.add_label,0)

        self.player_id_label = QLabel("PLAYER ID")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.player_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.player_id_label,2)

        self.equipment_id_label = QLabel("CODE NAME")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.equipment_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.equipment_id_label,2)

        self.equipment_id_label = QLabel("EQUIPMENT ID")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: darkred;")
        self.equipment_id_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.red_team_info_layout.addWidget(self.equipment_id_label,2)


        self.red_team_layout.addLayout(self.red_team_info_layout)
        
        self.red_team_list = QGridLayout()
        self.red_row = []

        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field3 = QLineEdit()

            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field3.setStyleSheet("background-color: white; color: black;")

            num_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            input_field1.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            input_field2.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            input_field3.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: white;")
            arrow_label.setVisible(False)
            arrow_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            # Adds row to the red_row list and to the GUI
            self.red_row.append((arrow_label, num_label, input_field1, input_field2, input_field3))
            self.red_team_list.addWidget(arrow_label, i, 0)
            self.red_team_list.addWidget(num_label, i, 1)
            self.red_team_list.addWidget(input_field1, i, 2)
            self.red_team_list.addWidget(input_field2, i, 3)
            self.red_team_list.addWidget(input_field3, i, 4)
        
        self.red_team_layout.addLayout(self.red_team_list)
        teams_layout.addLayout(self.red_team_layout)
        
        self.green_team_layout = QVBoxLayout()

        self.green_team_title = QLabel("Green TEAM")
        self.green_team_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_layout.addWidget(self.green_team_title)

        self.green_team_info_layout = QHBoxLayout()

        self.player_id_label = QLabel("")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.player_id_label.setFixedWidth(37)
        self.green_team_info_layout.addWidget(self.player_id_label,0)

        self.player_id_label = QLabel("PLAYER ID")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.player_id_label,2)

        self.equipment_id_label = QLabel("CODE NAME")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.equipment_id_label,2)

        self.equipment_id_label = QLabel("EQUIPMENT ID")
        self.equipment_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equipment_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_info_layout.addWidget(self.equipment_id_label,2)

        self.green_team_layout.addLayout(self.green_team_info_layout)
        
        self.green_team_list = QGridLayout()
        self.green_row = []
        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field3 = QLineEdit()

            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field3.setStyleSheet("background-color: white; color: black;")

            num_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            input_field1.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            input_field2.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            input_field3.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")
            arrow_label.setStyleSheet("font-weight: bold; color: white;")
            arrow_label.setVisible(False)
            arrow_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            # Adds row to the red_row list and to the GUI
            self.green_row.append((arrow_label, num_label, input_field1, input_field2, input_field3))
            self.green_team_list.addWidget(arrow_label, i, 0)
            self.green_team_list.addWidget(num_label, i, 1)
            self.green_team_list.addWidget(input_field1, i, 2)
            self.green_team_list.addWidget(input_field2, i, 3)
            self.green_team_list.addWidget(input_field3, i, 4)

        self.green_team_layout.addLayout(self.green_team_list)
        teams_layout.addLayout(self.green_team_layout)
        
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.directions)
        
        self.button_layout = QHBoxLayout()
        self.buttons = {}

        button_labels = {
                    1: "F1: Clear Game",
                    2: "F2: Change IP",
                    3: "F3: Start Game"
                }
        
        for index, label in button_labels.items():
            button = QPushButton(label)
            button.setStyleSheet("background-color: white; color: green; font-size: 12px;")
            button.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
            self.button_layout.addWidget(button)
            self.buttons[index] = button 
        
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)

        self.buttons[1].clicked.connect(self.clear_game)
        self.buttons[2].clicked.connect(self.change_ip_popup)
        self.buttons[3].clicked.connect(self.start_game)


    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        # Handler for the F1 key press
        if key == 16777264:
            self.clear_game()
        # Handler for the F2 key press
        elif key == 16777265:
            self.change_ip_popup()
        # Handler for the F3 key press
        elif key == 16777266:
            self.start_game()
        # Handler for the Enter key press
        elif key == 16777220:
            enter_field1 = None
            enter_field2 = None
            enter_field3 = None

            # Iterates through the red rows to look for cursor focus
            for arrow_label, num_label, field1, field2, field3 in self.red_row:
                if(field1.hasFocus() or field2.hasFocus() or field3.hasFocus()):
                    enter_field1 = field1
                    enter_field2 = field2
                    enter_field3 = field3

                    self.tab_ind = int(num_label.text())
                    self.team_red = True

            # Iterates through the green rows to look for cursor focus
            for arrow_label, num_label, field1, field2, field3 in self.green_row:
                if(field1.hasFocus() or field2.hasFocus() or field3.hasFocus()):
                    enter_field1 = field1
                    enter_field2 = field2
                    enter_field3 = field3

                    self.tab_ind = int(num_label.text())
                    self.team_red = False

            self.db.enter_handler(
                enter_field1, 
                enter_field2, 
                enter_field3, 
                self.directions, 
                self.tab_ind, 
                self.team_red, 
                self.red_row, 
                self.green_row
            )
            if enter_field3 and enter_field3.text():
                self.UDPBroadcast.sendto(str.encode(str(enter_field3.text())), self.broadcast)
                print(f'Broadcasting on port {self.broadcast_port}: {enter_field3.text()}')

        super().keyPressEvent(event)

    # Handles the clear game button functionality
    def clear_game(self):
        for arrow_label, num_label, field1, field2, field3 in self.red_row:
            field1.setText("")
            field2.setText("")
            field3.setText("")

        for arrow_label, num_label, field1, field2, field3 in self.green_row:
            field1.setText("")
            field2.setText("")
            field3.setText("")

        self.directions.setText(f"Enter a NEW PLAYER ID:")
        self.team_red = True
        self.red_row[0][2].setFocus()

    def ip_check(self, ip_input, popup, label):
        try:
            ipaddress.ip_address(ip_input.text())
            popup.accept()
            self.network = ip_input.text()
            self.broadcast = (self.network, self.broadcast_port)

        except ValueError:
            ip_input.setText("")
            label.setText("Invalid IP address entered. Try again.")


    # Handles the change IP button functionality
    def change_ip_popup(self):
         
        """ Show a popup dialog for entering a new server IP. """
        popup = QDialog(self)
        popup.setWindowTitle("Change Server IP")
        popup.setModal(True)
        popup.setStyleSheet("background-color: black; color: white;")
        popup.resize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("Enter new server IP:")
        layout.addWidget(label)

        ip_input = QLineEdit()
        ip_input.setPlaceholderText("e.g., 192.168.1.10")
        layout.addWidget(ip_input)

        button_layout = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(lambda: self.ip_check(ip_input, popup, label))
        button_layout.addWidget(confirm_button)

        layout.addLayout(button_layout)
        popup.setLayout(layout)
        popup.exec()

    # Collects player data into two lists
    def get_player_data(self):
        red_players = []
        green_players = []

        for row in self.red_row:
            player_id = row[2].text().strip()
            code_name = row[3].text().strip()
            equip_id = row[4].text().strip()
            if player_id and code_name and equip_id:
                red_players.append((player_id, code_name, equip_id))

        for row in self.green_row:
            player_id = row[2].text().strip()
            code_name = row[3].text().strip()
            equip_id = row[4].text().strip()
            if player_id and code_name and equip_id: 
                green_players.append((player_id, code_name, equip_id))

        return red_players, green_players


# Runs an instance of the PlayerEntryScreen (for testing purposes)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    sys.exit(app.exec())
