from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QGridLayout,QLineEdit,QSizePolicy, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer,QMetaObject,QEvent
from functools import partial
import sys
import signal
from pynput import keyboard
import psycopg2
from psycopg2 import sql



def on_key_event(key):
    #print(f"Key pressed: {event.name}")
    try:
        if key == keyboard.Key.f3:
            print("Start game")
            
        elif key == keyboard.Key.f1:
            print("Back to loading screen")
        elif key == keyboard.Key.tab:
            #main_window.change_tab_ind()
            QTimer.singleShot(0, self.change_tab_ind)  
            #print(main_window.tab_ind)
        elif key == keyboard.Key.esc:
            QMetaObject.invokeMethod(self.timer, "stop", Qt.ConnectionType.QueuedConnection)
            QMetaObject.invokeMethod(QApplication.instance(), "quit", Qt.ConnectionType.QueuedConnection)
        elif key == keyboard.Key.enter:
            #print("test")
                QTimer.singleShot(0, self.add_player_by_key)
    except AttributeError:  
        print("test")
        #name


class PlayerEntryScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Entry Screen")
        self.setGeometry(100, 100, 800, 600)
        #self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.tab_ind = 0
        self.popup_active = False 
        self.last_player_id = None
        QApplication.setStyle("windows")  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(0)  
        
        main_layout = QVBoxLayout()
        
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

        self.add_label = QLabel("ADD")
        self.add_label.setFixedWidth(78)
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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)
            """
            if (i != 0):
                input_field1.setReadOnly(True)
                input_field2.setReadOnly(True)
                
            input_field1.setReadOnly(True)
            """
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")

            self.red_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.red_team_list.addWidget(arrow_label, i, 1)
            self.red_team_list.addWidget(checkbox, i, 0)
            self.red_team_list.addWidget(num_label, i, 2)
            self.red_team_list.addWidget(input_field1, i, 3)
            self.red_team_list.addWidget(input_field2, i, 4)
            self.red_team_list.addWidget(input_field3, i, 5)
            #input_field2.textChanged.connect(self.check_inputs)
            # Connect stateChanged with partial to pass the checkbox itself
            field=input_field1
            field2=input_field2 
            field3=input_field3
            player_num=i
            team="Red"
            checkbox.stateChanged.connect(
                partial(self.on_checkbox_toggled, checkbox, field, field2, field3, player_num, team)
            )
            #checkbox.stateChanged.connect(lambda state, field=input_field1, field2=input_field2, player_num=i, team="Red": self.on_checkbox_toggled(state, field, field2, player_num, team))


        self.red_team_layout.addLayout(self.red_team_list)
        teams_layout.addLayout(self.red_team_layout)
        
        self.green_team_layout = QVBoxLayout()

        self.green_team_title = QLabel("Green TEAM")
        self.green_team_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_team_title.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.green_team_layout.addWidget(self.green_team_title)

        self.green_team_info_layout = QHBoxLayout()

        self.player_id_label = QLabel("ADD")
        self.player_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_id_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: Green;")
        self.player_id_label.setFixedWidth(78)
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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)
            """
            if (i != 0):
                input_field1.setReadOnly(True)
                input_field2.setReadOnly(True)
                
            input_field1.setReadOnly(True)
            """
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            self.green_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.green_team_list.addWidget(checkbox, i, 0)
            self.green_team_list.addWidget(arrow_label, i, 1)
            self.green_team_list.addWidget(num_label, i, 2)
            self.green_team_list.addWidget(input_field1, i, 3)
            self.green_team_list.addWidget(input_field2, i, 4)
            self.green_team_list.addWidget(input_field3, i, 5)
            #input_field2.textChanged.connect(self.check_inputs)
            field=input_field1
            field2=input_field2 
            fiedl3=input_field3
            player_num=i
            team="Green"
            checkbox.stateChanged.connect(
                partial(self.on_checkbox_toggled, checkbox, field, field2,fiedl3, player_num, team)
            )
            #checkbox.stateChanged.connect(lambda state, field=input_field1, field2=input_field2, player_num=i, team="Green": self.on_checkbox_toggled(state, field, field2, player_num, team))


        self.green_team_layout.addLayout(self.green_team_list)
        teams_layout.addLayout(self.green_team_layout)
        
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.directions)
        
        self.button_layout = QHBoxLayout()
        self.buttons = {}
        button_labels = {
                    30: "F1 Edit Game",
                    31: "F2 Game Parameters",
                    32: "F3 Start Game",
                    33: "F5 PreEntered Games",
                    34: "F7",
                    35: "F8 View Game",
                    36: "F10 Flick Sync",
                    37: "F12 Clear Game"
                }        
        for index, label in button_labels.items():
            button = QPushButton(label)
            button.setStyleSheet("background-color: white; color: green; font-size: 12px;")
            button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.button_layout.addWidget(button)
            self.buttons[index] = button 
        
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)
        self.install_input_event_listeners() 
        self.install_button_event_listeners()

        
    def add_player_by_key(self):
        for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
        for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")
        if self.tab_ind >= 30:
            return

        team = "Red" if self.tab_ind % 2 == 0 else "Green"
        row_index = self.tab_ind // 2  

        if team == "Red":
            row = self.red_row[row_index]
        else:
            row = self.green_row[row_index]

        checkbox, arrow_label, num_label, player_id_field, code_name_field, equip_id = row
        
        self.on_checkbox_toggled(
            checkbox,  
            player_id_field,  
            code_name_field, 
            equip_id,
            row_index,  
            team,  
            Qt.CheckState.Unchecked  
        )

        checkbox.setCheckState(Qt.CheckState.Checked) 
        #print("test3", main_window.tab_ind)
        #print("test",self.red_row[main_window.tab_ind][5].text())
        self.red_row[int((self.tab_ind)/2)][1].setStyleSheet("color: black;")
        self.green_row[int((self.tab_ind-1)/2)][1].setStyleSheet("color: black;")
        QApplication.processEvents()

        print(f"Equipment ID Field Value: {equip_id.text()}")  

        

                
    def change_tab_ind(self):
                self.tab_ind +=1
                if (self.tab_ind == 38):
                    self.tab_ind = 0

                if (self.tab_ind < 30):
                    if (self.tab_ind%2==0):
                        if(self.red_row[(self.tab_ind) // 2][3].text() == ""):
                            target_input = self.red_row[(self.tab_ind) // 2][3]
                        elif (self.red_row[(self.tab_ind) // 2][4].text() == ""):
                             target_input = self.red_row[(self.tab_ind) // 2][4]
                        else: 
                             target_input = self.red_row[(self.tab_ind) // 2][5]

                        #print(target_input)
                        QMetaObject.invokeMethod(target_input, "setFocus", Qt.ConnectionType.QueuedConnection)
                        for row_index, row in enumerate(self.red_row): 
                            row[1].setStyleSheet("color: black;")
                        for row_index, row in enumerate(self.green_row):  
                            row[1].setStyleSheet("color: black;")
                        self.red_row[(self.tab_ind) // 2][1].setStyleSheet("color: white;")

                    elif(self.tab_ind%2==1):
                        if(self.green_row[(self.tab_ind) // 2][3].text() == ""):
                            target_input = self.green_row[(self.tab_ind) // 2][3]
                        elif (self.red_row[(self.tab_ind) // 2][4].text() == ""):
                             target_input = self.green_row[(self.tab_ind) // 2][4]
                        else: 
                             target_input = self.green_row[(self.tab_ind) // 2][5]
                        #print(target_input)
                        
                        QMetaObject.invokeMethod(target_input, "setFocus", Qt.ConnectionType.QueuedConnection)
                        for row_index, row in enumerate(self.red_row): 
                            row[1].setStyleSheet("color: black;")
                        for row_index, row in enumerate(self.green_row):  
                            row[1].setStyleSheet("color: black;")
                        self.green_row[(self.tab_ind) // 2][1].setStyleSheet("color: white;")


                for button in self.buttons.values():
                    button.setStyleSheet("background-color: white; color: green; font-size: 12px;")

                if self.tab_ind in self.buttons or self.tab_ind == 30:
                    button = self.buttons[self.tab_ind]

                    button.setStyleSheet("background-color: grey; color: black;")
                    button.setDefault(True) 

    def check_inputs(self):
            for arrow_label, num_label, input1, input2 in self.red_row:
                index = int(num_label.text())
                if (input2.text().strip() != "" or index == 30):
                    self.red_row[index+1][2].setReadOnly(False)

            for arrow_label, num_label, input1, input2 in self.green_row:
                index = int(num_label.text())
                if  input2.text().strip() != "" or index == 30:
                    self.green_row[index+1][2].setReadOnly(False)

    def toggle_visibility(self):        
            combined_rows = self.red_row + self.green_row  
            
            for index, (arrow_label, checkbox, num_label, input1, input2, input3) in enumerate(combined_rows):
                row_index = int(num_label.text()) if num_label.text() else index  

                if self.tab_ind % 2 == 0:

                    if (self.tab_ind // 2) < len(self.red_row):
                        #self.red_row[main_window.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[(self.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: black;")

                elif self.tab_ind % 2 == 1:

                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        #self.green_row[(main_window.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: white;")
                        self.green_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if (self.tab_ind // 2) < len(self.red_row):
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: black;")

                else:
                    if index // 2 < len(self.red_row):
                        self.red_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")
                    if index // 2 < len(self.green_row):
                        self.green_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")

    def sort_players(self):
            for i in range(len(self.red_row) - 1):
                checkbox, arrow_label, num_label, player_id_field, code_name_field,equip_id = self.red_row[i]

                if player_id_field.text().strip() == "" and code_name_field.text().strip() == "":
                    for j in range(i + 1, len(self.red_row)):
                        next_checkbox, next_arrow, next_num, next_player_id, next_code_name, next_eqip_id = self.red_row[j]

                        if next_player_id.text().strip() != "" or next_code_name.text().strip() != "" or next_eqip_id.text().strip() != "":
                            QTimer.singleShot(0, self.change_tab_ind) 
                            player_id_field.setText(next_player_id.text())
                            player_id_field.setReadOnly(True)
                            code_name_field.setText(next_code_name.text())
                            code_name_field.setReadOnly(True)
                            equip_id.setText(next_eqip_id.text())
                            equip_id.setReadOnly(True)

                            next_player_id.clear()
                            next_player_id.setReadOnly(False)
                            next_code_name.clear()
                            next_code_name.setReadOnly(True)
                            next_eqip_id.clear()
                            next_eqip_id.setReadOnly(True)

                            checkbox.setChecked(True)
                            checkbox.setCheckState(Qt.CheckState.Checked)
                            next_checkbox.setChecked(False)
                            next_checkbox.setCheckState(Qt.CheckState.Unchecked)
                            next_checkbox.setEnabled(True)
                            
                            break 
            for i in range(len(self.green_row) - 1):
                checkbox, arrow_label, num_label, player_id_field, code_name_field, equip_id  = self.green_row[i]

                if player_id_field.text().strip() == "" and code_name_field.text().strip() == "":
                    for j in range(i + 1, len(self.green_row)):
                        next_checkbox, next_arrow, next_num, next_player_id, next_code_name, next_eqip_id = self.green_row[j]

                        if next_player_id.text().strip() != "" or next_code_name.text().strip() != "" or next_eqip_id.text().strip() != "":
                            QTimer.singleShot(0, self.change_tab_ind) 
                            player_id_field.setText(next_player_id.text())
                            player_id_field.setReadOnly(True)
                            code_name_field.setText(next_code_name.text())
                            code_name_field.setReadOnly(True)
                            equip_id.setText(next_eqip_id.text())
                            equip_id.setReadOnly(True)

                            next_player_id.clear()
                            next_player_id.setReadOnly(False)
                            next_code_name.clear()
                            next_code_name.setReadOnly(True)
                            next_eqip_id.clear()
                            next_eqip_id.setReadOnly(True)

                            checkbox.setChecked(True)
                            checkbox.setCheckState(Qt.CheckState.Checked)
                            next_checkbox.setChecked(False)
                            next_checkbox.setCheckState(Qt.CheckState.Unchecked)
                            next_checkbox.setEnabled(True)
                            
                            break 

    def on_checkbox_toggled(self, checkbox, field, field2, field3, player_num, team, state):
        #database check here
        player_id = field.text().strip()
        code_name = field2.text().strip()
        equip_id = field3.text().strip()

        DB_NAME = "photon"
        DB_HOST = "127.0.0.1"
        DB_PORT = "5432"  # PostgreSQL default port

        def connect():
            """Establish a connection to the PostgreSQL database."""
            print("Attempting to connect to PostgreSQL...")
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    host=DB_HOST,
                    user="student",
                    password="student",
                    port=DB_PORT
                )
                print("Connected to PostgreSQL successfully!")
                return conn
            except psycopg2.Error as e:
                print("Database connection failed:", e)
                return None

        def get_player_by_id(conn, player_id):
            """Check if a player exists in the database by player ID using an existing connection."""
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None  # Return codename if found, otherwise None
            return None

        def add_new_player(conn, player_id, codename):
            """Insert a new player into the database using an existing connection."""
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                cursor.close()
                print(f"Player '{codename}' (ID: {player_id}) added successfully!")


        def get_all_players():
            """Retrieve all players from the database."""
            conn = connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM players;")
                players = cursor.fetchall()
                cursor.close()
                conn.close()
                return players  
            return []


        text = self.directions.text()
        number = text.replace("Enter ", "").replace("'s CODE NAME:", "")
       
        if "CODE NAME:" in self.directions.text() and field.text() != number:
                field.setText("")
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                return
        elif player_id == "":
                self.directions.setText("Player Does not have an ID")
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                return

        elif code_name == "":  
                conn = connect()
                if conn:
                    player = get_player_by_id(conn, player_id)
                    print("get player ID")
                    
                    if player:  
                        field2.setText(player)
                    else: 
                        add_new_player(conn, player_id, code_name)

                    conn.close()  
                field.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QMetaObject.invokeMethod(field2, "setFocus", Qt.ConnectionType.QueuedConnection)
                field2.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                return
        elif equip_id == "":
                field2.setReadOnly(True)
                self.directions.setText(f"Enter {player_id} equipment ID") 
                QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                field3.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                return
        else:
            checkbox.setEnabled(False)
            self.sort_players()
            field2.setReadOnly(True)
            #QTimer.singleShot(0, main_window.change_tab_ind) 

        # if not self.popup_active:  
                
                #self.show_popup_input(player_id, code_name)
            field3.setReadOnly(True)
            QTimer.singleShot(0, self.change_tab_ind) 

            self.popup_active = False


    def show_popup_input(self, player_id, code_name):
            if self.popup_active: 
                return
            
            if (not self.last_player_id == "") and (self.last_player_id == player_id):
                return

            self.last_player_id = player_id

            self.popup_active = True 
            popup = QDialog(self)
            popup.setWindowTitle("Enter Equipment ID")
            popup.setModal(True)  
            popup.setStyleSheet("background-color: black; color: white;")  
            popup.resize(400, 200)  

            layout = QVBoxLayout()

            self.directions.setText(f"Player {player_id} - Equipment ID")
            label = QLabel(f"Enter Equipment ID for Player {player_id}\nCODE NAME: {code_name}")
            layout.addWidget(label)

            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter Equipment ID...")
            layout.addWidget(input_field)

            button_layout = QHBoxLayout()

            confirm_button = QPushButton("Confirm")
            confirm_button.clicked.connect(lambda: self.process_equipment_id(popup, player_id, code_name, input_field.text()))
            button_layout.addWidget(confirm_button)

            layout.addLayout(button_layout)
            popup.setLayout(layout)

            popup.exec()  
            self.popup_active = False 

    def process_equipment_id(self, popup, player_id, code_name, equipment_id):
        if not player_id or not code_name or not equipment_id:
            print("⚠️ All fields must be filled!")
            return  

        try:
            player_id = int(player_id)  
        except ValueError:
            print("⚠️ Player ID must be a number!")
            return

        team = "red" if player_id % 2 == 0 else "green"  


        popup.accept()
  

    def install_input_event_listeners(self):
            for row in self.red_row + self.green_row: 
                row[3].installEventFilter(self)  
                row[4].installEventFilter(self)
                row[5].installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if isinstance(obj, QLineEdit):
                for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
                for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")
                     
                for row_index, row in enumerate(self.red_row):  
                    if obj in (row[3], row[4], row[5]):  
                        self.tab_ind = row_index * 2 
                        row[1].setStyleSheet("color: white;")
                        self.tab_to_target_red(row_index * 2)
                        return True
                
                for row_index, row in enumerate(self.green_row):  
                    if obj in (row[3], row[4], row[5]):  
                        self.tab_ind = row_index * 2 + 1 
                        row[1].setStyleSheet("color: white;")
                        self.tab_to_target_green(row_index * 2 + 1)
                        return True  
                    
                for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
                for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")

        return super().eventFilter(obj, event)  
    

    def tab_to_target_red(self, target_index, extra_steps=0):
        if self.tab_ind != target_index or extra_steps > 0:
            self.change_tab_ind()  

            if extra_steps > 0:
                extra_steps -= 1  
            
            QTimer.singleShot(0, lambda: self.tab_to_target_red(target_index, extra_steps))  


    def tab_to_target_green(self, target_index, extra_steps=0):
        if self.tab_ind != target_index or extra_steps > 0:
            self.change_tab_ind()  

            if extra_steps > 0:
                extra_steps -= 1  
            
            QTimer.singleShot(0, lambda: self.tab_to_target_green(target_index, extra_steps)) 

    def install_button_event_listeners(self):
        for index, button in self.buttons.items():
            button.clicked.connect(partial(self.on_button_clicked, index, button))

    def on_button_clicked(self, index, button):
        self.directions.setText(f"Button {index} clicked: {button.text()}")

        if index == 30:  # F1 Edit Game
            print("Editing Game...")
            for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")

            QApplication.processEvents()
            self.tab_ind = 30 
            QTimer.singleShot(0, lambda: self.tab_to_target_red(30, 0))  


            
        elif index == 31:  # F2 Game Parameters
            print("Adjusting Game Parameters...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 31
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(31, 0)) 
        elif index == 32:  # F3 Start Game
            print("Starting Game...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 32
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(32, 0)) 
        elif index == 33:  # F5 PreEntered Games
            print("Viewing PreEntered Games...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 33
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(33, 0)) 
        elif index == 34:  # F7
            print("F7 Action Triggered")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 34
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(34, 0))            
        elif index == 35:  # F8 View Game
            print("Viewing Game...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 35
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(35, 0))           
        elif index == 36:  # F10 Flick Sync
            print("Performing Flick Sync...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(36, 0))
            self.tab_ind = 36   
            QApplication.processEvents()           
        elif index == 37:  # F12 Clear Game
            print("Clearing Game...")
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 37   
            QApplication.processEvents() 
            QTimer.singleShot(0, lambda: self.tab_to_target_red(37, 0))         

if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    QMetaObject.invokeMethod(self.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection)
    listener = keyboard.Listener(on_press=on_key_event)
    listener.start()
    timer = QTimer()
    timer.timeout.connect(self.toggle_visibility)
    timer.start(100)

    sys.exit(app.exec())
