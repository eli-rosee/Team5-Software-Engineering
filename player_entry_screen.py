from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QGridLayout,QLineEdit,QSizePolicy, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer,QMetaObject,QEvent
from functools import partial
import sys
import time
import socket
from pynput import keyboard
import psycopg2
from psycopg2 import sql
from client import PhotonNetwork  
import server
from play_action_screen import PlayActionScreen 
from countdown import CountdownWindow

from PyQt6.QtCore import QThread, pyqtSignal

class sortPlayers(QThread):
    finished = pyqtSignal(list, list)  # Signal to return sorted data

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        red_sorted, green_sorted = self.parent.sort_players()
        self.finished.emit(red_sorted, green_sorted) 

class ChangeTabInd(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.change_tab_ind()
        self.finished.emit() 

class PlayerEntryScreen(QWidget):
    photon_network_instance = None

    def create_photon_network(self):
        from client import PhotonNetwork 
        
        if PlayerEntryScreen.photon_network_instance is None:
            PlayerEntryScreen.photon_network_instance = PhotonNetwork(server_ip="127.0.0.1", server_port=7500, client_port=7501)

        return PlayerEntryScreen.photon_network_instance 
    
    def __init__(self, photon_network=None):
        super().__init__()
        self.change_tab_thread = ChangeTabInd(self) 
        self.setWindowTitle("Player Entry Screen")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.tab_ind = 0
        self.popup_active = False 
        self.last_player_id = None
        QApplication.setStyle("windows") 
        
        if photon_network is None:
            if PlayerEntryScreen.photon_network_instance is None:
                PlayerEntryScreen.photon_network_instance = self.create_photon_network()
            self.photon_network = PlayerEntryScreen.photon_network_instance 
        else:
            self.photon_network = photon_network

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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            checkbox.setVisible(False)

            self.red_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.red_team_list.addWidget(arrow_label, i, 1)
            self.red_team_list.addWidget(checkbox, i, 0)
            self.red_team_list.addWidget(num_label, i, 2)
            self.red_team_list.addWidget(input_field1, i, 3)
            self.red_team_list.addWidget(input_field2, i, 4)
            self.red_team_list.addWidget(input_field3, i, 5)
    
            field=input_field1
            field2=input_field2 
            field3=input_field3
            player_num=i
            team="Red"
            self.on_checkbox_toggled(checkbox, field, field2, field3, player_num, team, Qt.CheckState.Checked)
        
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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            checkbox.setVisible(False)
            self.green_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.green_team_list.addWidget(checkbox, i, 0)
            self.green_team_list.addWidget(arrow_label, i, 1)
            self.green_team_list.addWidget(num_label, i, 2)
            self.green_team_list.addWidget(input_field1, i, 3)
            self.green_team_list.addWidget(input_field2, i, 4)
            self.green_team_list.addWidget(input_field3, i, 5)

            field=input_field1
            field2=input_field2 
            fiedl3=input_field3
            player_num=i
            team="Green"
            self.on_checkbox_toggled(checkbox, field, field2, field3, player_num, team, Qt.CheckState.Checked)


        self.green_team_layout.addLayout(self.green_team_list)
        teams_layout.addLayout(self.green_team_layout)
        
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.directions)
        
        self.button_layout = QHBoxLayout()
        self.buttons = {}
        button_labels = {
                    30: "F1",
                    31: "F2",
                    32: "F3",
                    33: "F5 Start Game",
                    34: "Change IP",
                    35: "F8",
                    36: "F10",
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
        self.count = 0

    #player action screen
    def get_player_data(self):
        red_players = []
        green_players = []

        for row in self.red_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()
            if player_id and code_name and equip_id: 
                red_players.append((player_id, code_name, equip_id))

        for row in self.green_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()
            if player_id and code_name and equip_id: 
                green_players.append((player_id, code_name, equip_id))

        return red_players, green_players
    
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
        self.red_row[int((self.tab_ind)/2)][1].setStyleSheet("color: black;")
        self.green_row[int((self.tab_ind-1)/2)][1].setStyleSheet("color: black;")
        QApplication.processEvents()

        if (equip_id.text() != ""):
            try:
                equip_id_value = int(equip_id.text().strip()) 
                self.photon_network.equipID(equip_id.text())
            except ValueError: 
                print("Error: equip_id contains non-numeric text")
                
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
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[(self.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: black;")

                elif self.tab_ind % 2 == 1:

                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if (self.tab_ind // 2) < len(self.red_row):
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: black;")

                else:
                    if index // 2 < len(self.red_row):
                        self.red_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")
                    if index // 2 < len(self.green_row):
                        self.green_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")

    def sort_players(self):
        """ Sorts players without modifying UI directly """
        red_sorted = []
        green_sorted = []

        # Process Red Team
        for i in range(len(self.red_row)):
            player_id = self.red_row[i][3].text().strip()
            code_name = self.red_row[i][4].text().strip()
            equip_id = self.red_row[i][5].text().strip()

            if player_id and code_name and equip_id:
                red_sorted.append((player_id, code_name, equip_id))

        # Process Green Team
        for i in range(len(self.green_row)):
            player_id = self.green_row[i][3].text().strip()
            code_name = self.green_row[i][4].text().strip()
            equip_id = self.green_row[i][5].text().strip()

            if player_id and code_name and equip_id:
                green_sorted.append((player_id, code_name, equip_id))

        return red_sorted, green_sorted
    def on_checkbox_toggled(self, checkbox, field, field2, field3, player_num, team, state):
        player_id = field.text().strip()
        code_name = field2.text().strip()
        equip_id = field3.text().strip()
        
        DB_NAME = "photon"
        DB_HOST = "127.0.0.1"
        DB_PORT = "5432"  

        def connect():
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    host=DB_HOST,
                    user="student",
                    password="student",
                    port=DB_PORT
                )
                return conn
            except psycopg2.Error as e:
                print("Database connection failed:", e)
                return None

        def get_player_by_id(conn, player_id):
            if conn:
                cursor = conn.cursor()
                player_id = int(player_id)
                cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None  
            return None

        def add_new_player(conn, player_id, codename):
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                cursor.close()


        def get_all_players():
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

        elif code_name == "" and player_id!="":
                conn = connect()
                if conn:
                        player = get_player_by_id(conn, player_id)
                        if player:  
                            field2.setText(player)
                            field2.setReadOnly(True)
                            self.directions.setText(f"Enter {player_id} equipment ID") 
                            QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                            field3.setReadOnly(False)
                            checkbox.setCheckState(Qt.CheckState.Unchecked)
                            self.count +=1
                            QApplication.processEvents()

                            QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                            QApplication.processEvents()
                            return
                        else: 
                            field2.setText("")

                        conn.close()  

                field.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QApplication.processEvents()
                QMetaObject.invokeMethod(field2, "setFocus", Qt.ConnectionType.QueuedConnection)
                QApplication.processEvents()
                field2.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.count +=1
                return
        elif (equip_id=="" and code_name!="" and player_id!=""):
                conn = connect()
                if conn:
                    player = get_player_by_id(conn, player_id)                            
                    if player:  
                        field2.setText(player)
                    else: 
                        add_new_player(conn, player_id, code_name)

                conn.close()  

                field2.setReadOnly(True)
                self.directions.setText(f"Enter {player_id} equipment ID") 
                QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                field3.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.count +=1
                return
        else:
            self.directions.setText(f"Enter a NEW PLAYER ID:") 
            if hasattr(self, "worker") and self.worker.isRunning():
                return

            self.worker = sortPlayers(self)
            self.worker.start()
            
            field2.setReadOnly(True)
            field3.setReadOnly(True)
            self.change_tab_thread.start()
            self.popup_active = False
  

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
            self.change_tab_thread.start()
            if extra_steps > 0:
                extra_steps -= 1  
            QTimer.singleShot(0, lambda: self.tab_to_target_red(target_index, extra_steps))  


    def tab_to_target_green(self, target_index, extra_steps=0):
        if self.tab_ind != target_index or extra_steps > 0:
            self.change_tab_thread.start()
            if extra_steps > 0:
                extra_steps -= 1  
            QTimer.singleShot(0, lambda: self.tab_to_target_green(target_index, extra_steps)) 

    def install_button_event_listeners(self):
        for index, button in self.buttons.items():
            button.clicked.connect(partial(self.on_button_clicked, index, button))

    def clear_all_players(self):
        for checkbox, arrow_label, num_label, player_id_field, code_name_field, equip_id in self.red_row + self.green_row:
            player_id_field.clear()
            player_id_field.setReadOnly(False)
            code_name_field.clear()
            equip_id.clear()


        QApplication.processEvents()

    def open_play_action_screen(self):
        red_players, green_players = self.get_player_data()
        self.play_action_screen = PlayActionScreen(red_players, green_players, self.photon_network, self)
        self.hide()
        self.play_action_screen.showMaximized()

    def finish_countdown(self):
        self.countdown_screen.hide()
        red_players, green_players = self.get_player_data()

        self.play_action_screen = PlayActionScreen(
            red_players, 
            green_players, 
            self.photon_network,  
            player_entry_screen_instance=self  
        )
        self.play_action_screen.showMaximized()

    def on_button_clicked(self, index, button):
        self.directions.setText(f"Button {index} clicked: {button.text()}")

        if index == 30:  #F1
            for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")

            QApplication.processEvents()
            self.tab_ind = 30 
            QTimer.singleShot(0, lambda: self.tab_to_target_red(30, 0))    
        elif index == 31:  # F2 
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 31
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(31, 0)) 
        elif index == 32:  # F3
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 32
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(32, 0)) 
        elif index == 33:  # F5
            red_players, green_players = self.get_player_data()
            missing_data = False

            for row in self.red_row + self.green_row:  
                player_id = row[3].text().strip()
                code_name = row[4].text().strip()
                equip_id = row[5].text().strip()

                if player_id and (not code_name or not equip_id):  
                    missing_data = True  
                    break  

            if not red_players or not green_players:
                self.directions.setText("There is an empty team")
            elif missing_data:
                self.directions.setText("Please fill in all equipment IDs and codenames before starting the game")
            else:
                self.hide()
                self.countdown_screen = CountdownWindow(self)
                self.countdown_screen.showFullScreen()
                QTimer.singleShot(30000, self.finish_countdown)
                
                from music import music_player
                QTimer.singleShot(25000, music_player.play_random_music)
                self.photon_network.send_start_signal()

                self.tab_ind = 33
                QApplication.processEvents()
                
        elif index == 34:  # F7
            print("Change IP")
            self.show_ip_input_dialog()
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 34
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(34, 0))            
        elif index == 35:  # F8
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 35
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(35, 0))           
        elif index == 36:  # F10
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(36, 0))
            self.tab_ind = 36   
            QApplication.processEvents()           
        elif index == 37:  # F12
            self.clear_all_players()  
    
    def is_valid_ip(self, ip):
         """Check if the given string is a valid IPv4 address."""
         try:
             socket.inet_aton(ip)
             return True
         except socket.error:
             return False
 
     
    def show_ip_input_dialog(self):
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
         confirm_button.clicked.connect(lambda: self.update_server_ip(popup, ip_input.text()))
         button_layout.addWidget(confirm_button)
 
         layout.addLayout(button_layout)
         popup.setLayout(layout)
         popup.exec()
 
    def update_server_ip(self, popup, new_ip):
         new_ip = ".".join(["0"] * (3 - new_ip.count(".")) + new_ip.split("."))
         if not self.is_valid_ip(new_ip.strip()):
             print("Invalid IP address entered.")
             error_popup = QDialog(self)
             error_popup.setWindowTitle("Error")
             error_popup.setModal(True)
             error_popup.setStyleSheet("background-color: black; color: white;")
             error_popup.resize(250, 100)
 
             layout = QVBoxLayout()
             error_label = QLabel("Invalid IP Address. Try again.")
             layout.addWidget(error_label)
 
             close_button = QPushButton("OK")
             close_button.clicked.connect(error_popup.close)
             layout.addWidget(close_button)
 
             error_popup.setLayout(layout)
             error_popup.exec()
             return  # Stop execution if IP is invalid
 
         popup.close()  # Close the input popup if valid
         self.photon_network.server_ip = new_ip.strip()
         self.photon_network.client_ip = new_ip.strip()
         print("changed to ", new_ip.strip())
         if PlayerEntryScreen.photon_network_instance:
            print("Closing existing network instance...")
            PlayerEntryScreen.photon_network_instance.close()
            
            time.sleep(1) 

         try:
            server.server_instance.restart_server(new_ip.strip())
            PlayerEntryScreen.photon_network_instance = PhotonNetwork(
            server_ip=new_ip, server_port=7500, client_port=7501
            )

            self.photon_network = PlayerEntryScreen.photon_network_instance 
            print(f"Successfully changed server IP to {new_ip}")
            self.photon_network.update_ip(new_ip)

         except socket.error as e:
            print(f"Error binding to new IP {new_ip}: {e}")

         #self.photon_network.update_ip(new_ip.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    QMetaObject.invokeMethod(self.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection)
    timer = QTimer()
    timer.timeout.connect(self.toggle_visibility)
    timer.start(100)

    sys.exit(app.exec())
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QGridLayout,QLineEdit,QSizePolicy, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer,QMetaObject,QEvent
from functools import partial
import sys
import time
import socket
from pynput import keyboard
import psycopg2
from psycopg2 import sql
from client import PhotonNetwork  
import server
from play_action_screen import PlayActionScreen 
from countdown import CountdownWindow

from PyQt6.QtCore import QThread, pyqtSignal

class sortPlayers(QThread):
    finished = pyqtSignal(list, list)  # Signal to return sorted data

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        red_sorted, green_sorted = self.parent.sort_players()
        self.finished.emit(red_sorted, green_sorted) 

class ChangeTabInd(QThread):
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.change_tab_ind()
        self.finished.emit() 

class PlayerEntryScreen(QWidget):
    photon_network_instance = None

    def create_photon_network(self):
        from client import PhotonNetwork 
        
        if PlayerEntryScreen.photon_network_instance is None:
            PlayerEntryScreen.photon_network_instance = PhotonNetwork(server_ip="127.0.0.1", server_port=7500, client_port=7501)

        return PlayerEntryScreen.photon_network_instance 
    
    def __init__(self, photon_network=None):
        super().__init__()
        self.change_tab_thread = ChangeTabInd(self) 
        self.setWindowTitle("Player Entry Screen")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")
        self.tab_ind = 0
        self.popup_active = False 
        self.last_player_id = None
        QApplication.setStyle("windows") 
        
        if photon_network is None:
            if PlayerEntryScreen.photon_network_instance is None:
                PlayerEntryScreen.photon_network_instance = self.create_photon_network()
            self.photon_network = PlayerEntryScreen.photon_network_instance 
        else:
            self.photon_network = photon_network

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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)

            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            checkbox.setVisible(False)

            self.red_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.red_team_list.addWidget(arrow_label, i, 1)
            self.red_team_list.addWidget(checkbox, i, 0)
            self.red_team_list.addWidget(num_label, i, 2)
            self.red_team_list.addWidget(input_field1, i, 3)
            self.red_team_list.addWidget(input_field2, i, 4)
            self.red_team_list.addWidget(input_field3, i, 5)
    
            field=input_field1
            field2=input_field2 
            field3=input_field3
            player_num=i
            team="Red"
            self.on_checkbox_toggled(checkbox, field, field2, field3, player_num, team, Qt.CheckState.Checked)
        
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
            input_field2.setReadOnly(True)
            input_field3.setReadOnly(True)
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            checkbox.setVisible(False)
            self.green_row.append((checkbox, arrow_label, num_label, input_field1, input_field2, input_field3))
            self.green_team_list.addWidget(checkbox, i, 0)
            self.green_team_list.addWidget(arrow_label, i, 1)
            self.green_team_list.addWidget(num_label, i, 2)
            self.green_team_list.addWidget(input_field1, i, 3)
            self.green_team_list.addWidget(input_field2, i, 4)
            self.green_team_list.addWidget(input_field3, i, 5)

            field=input_field1
            field2=input_field2 
            fiedl3=input_field3
            player_num=i
            team="Green"
            self.on_checkbox_toggled(checkbox, field, field2, field3, player_num, team, Qt.CheckState.Checked)


        self.green_team_layout.addLayout(self.green_team_list)
        teams_layout.addLayout(self.green_team_layout)
        
        main_layout.addLayout(teams_layout)
        main_layout.addWidget(self.directions)
        
        self.button_layout = QHBoxLayout()
        self.buttons = {}
        button_labels = {
                    30: "F1",
                    31: "F2",
                    32: "F3",
                    33: "F5 Start Game",
                    34: "Change IP",
                    35: "F8",
                    36: "F10",
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
        self.count = 0

    #player action screen
    def get_player_data(self):
        red_players = []
        green_players = []

        for row in self.red_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()
            if player_id and code_name and equip_id: 
                red_players.append((player_id, code_name, equip_id))

        for row in self.green_row:
            player_id = row[3].text().strip()
            code_name = row[4].text().strip()
            equip_id = row[5].text().strip()
            if player_id and code_name and equip_id: 
                green_players.append((player_id, code_name, equip_id))

        return red_players, green_players
    
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
        self.red_row[int((self.tab_ind)/2)][1].setStyleSheet("color: black;")
        self.green_row[int((self.tab_ind-1)/2)][1].setStyleSheet("color: black;")
        QApplication.processEvents()

        if (equip_id.text() != ""):
            try:
                equip_id_value = int(equip_id.text().strip()) 
                self.photon_network.equipID(equip_id.text())
            except ValueError: 
                print("Error: equip_id contains non-numeric text")
                
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
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[(self.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: black;")

                elif self.tab_ind % 2 == 1:

                    if ((self.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if (self.tab_ind // 2) < len(self.red_row):
                        self.red_row[self.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: black;")

                else:
                    if index // 2 < len(self.red_row):
                        self.red_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")
                    if index // 2 < len(self.green_row):
                        self.green_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")

    def sort_players(self):
        """ Sorts players without modifying UI directly """
        red_sorted = []
        green_sorted = []

        # Process Red Team
        for i in range(len(self.red_row)):
            player_id = self.red_row[i][3].text().strip()
            code_name = self.red_row[i][4].text().strip()
            equip_id = self.red_row[i][5].text().strip()

            if player_id and code_name and equip_id:
                red_sorted.append((player_id, code_name, equip_id))

        # Process Green Team
        for i in range(len(self.green_row)):
            player_id = self.green_row[i][3].text().strip()
            code_name = self.green_row[i][4].text().strip()
            equip_id = self.green_row[i][5].text().strip()

            if player_id and code_name and equip_id:
                green_sorted.append((player_id, code_name, equip_id))

        return red_sorted, green_sorted
    def on_checkbox_toggled(self, checkbox, field, field2, field3, player_num, team, state):
        player_id = field.text().strip()
        code_name = field2.text().strip()
        equip_id = field3.text().strip()
        
        DB_NAME = "photon"
        DB_HOST = "127.0.0.1"
        DB_PORT = "5432"  

        def connect():
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    host=DB_HOST,
                    user="student",
                    password="student",
                    port=DB_PORT
                )
                return conn
            except psycopg2.Error as e:
                print("Database connection failed:", e)
                return None

        def get_player_by_id(conn, player_id):
            if conn:
                cursor = conn.cursor()
                player_id = int(player_id)
                cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None  
            return None

        def add_new_player(conn, player_id, codename):
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                cursor.close()


        def get_all_players():
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

        elif code_name == "" and player_id!="":
                conn = connect()
                if conn:
                        player = get_player_by_id(conn, player_id)
                        if player:  
                            field2.setText(player)
                            field2.setReadOnly(True)
                            self.directions.setText(f"Enter {player_id} equipment ID") 
                            QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                            field3.setReadOnly(False)
                            checkbox.setCheckState(Qt.CheckState.Unchecked)
                            self.count +=1
                            QApplication.processEvents()

                            QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                            QApplication.processEvents()
                            return
                        else: 
                            field2.setText("")

                        conn.close()  

                field.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QApplication.processEvents()
                QMetaObject.invokeMethod(field2, "setFocus", Qt.ConnectionType.QueuedConnection)
                QApplication.processEvents()
                field2.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.count +=1
                return
        elif (equip_id=="" and code_name!="" and player_id!=""):
                conn = connect()
                if conn:
                    player = get_player_by_id(conn, player_id)                            
                    if player:  
                        field2.setText(player)
                    else: 
                        add_new_player(conn, player_id, code_name)

                conn.close()  

                field2.setReadOnly(True)
                self.directions.setText(f"Enter {player_id} equipment ID") 
                QMetaObject.invokeMethod(field3, "setFocus", Qt.ConnectionType.QueuedConnection)
                field3.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.count +=1
                return
        else:
            self.directions.setText(f"Enter a NEW PLAYER ID:") 
            if hasattr(self, "worker") and self.worker.isRunning():
                return

            self.worker = sortPlayers(self)
            self.worker.start()
            
            field2.setReadOnly(True)
            field3.setReadOnly(True)
            self.change_tab_thread.start()
            self.popup_active = False
  

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
            self.change_tab_thread.start()
            if extra_steps > 0:
                extra_steps -= 1  
            QTimer.singleShot(0, lambda: self.tab_to_target_red(target_index, extra_steps))  


    def tab_to_target_green(self, target_index, extra_steps=0):
        if self.tab_ind != target_index or extra_steps > 0:
            self.change_tab_thread.start()
            if extra_steps > 0:
                extra_steps -= 1  
            QTimer.singleShot(0, lambda: self.tab_to_target_green(target_index, extra_steps)) 

    def install_button_event_listeners(self):
        for index, button in self.buttons.items():
            button.clicked.connect(partial(self.on_button_clicked, index, button))

    def clear_all_players(self):
        for checkbox, arrow_label, num_label, player_id_field, code_name_field, equip_id in self.red_row + self.green_row:
            player_id_field.clear()
            player_id_field.setReadOnly(False)
            code_name_field.clear()
            equip_id.clear()


        QApplication.processEvents()

    def open_play_action_screen(self):
        red_players, green_players = self.get_player_data()
        self.play_action_screen = PlayActionScreen(red_players, green_players, self.photon_network, self)
        self.hide()
        self.play_action_screen.showMaximized()

    def finish_countdown(self):
        self.countdown_screen.hide()
        red_players, green_players = self.get_player_data()

        self.play_action_screen = PlayActionScreen(
            red_players, 
            green_players, 
            self.photon_network,  
            player_entry_screen_instance=self  
        )
        self.play_action_screen.showMaximized()

    def on_button_clicked(self, index, button):
        self.directions.setText(f"Button {index} clicked: {button.text()}")

        if index == 30:  #F1
            for row_index, row in enumerate(self.red_row): 
                     row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                     row[1].setStyleSheet("color: black;")

            QApplication.processEvents()
            self.tab_ind = 30 
            QTimer.singleShot(0, lambda: self.tab_to_target_red(30, 0))    
        elif index == 31:  # F2 
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 31
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(31, 0)) 
        elif index == 32:  # F3
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 32
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(32, 0)) 
        elif index == 33:  # F5
            red_players, green_players = self.get_player_data()
            missing_data = False

            for row in self.red_row + self.green_row:  
                player_id = row[3].text().strip()
                code_name = row[4].text().strip()
                equip_id = row[5].text().strip()

                if player_id and (not code_name or not equip_id):  
                    missing_data = True  
                    break  

            if not red_players or not green_players:
                self.directions.setText("There is an empty team")
            elif missing_data:
                self.directions.setText("Please fill in all equipment IDs and codenames before starting the game")
            else:
                self.hide()
                self.countdown_screen = CountdownWindow(self)
                self.countdown_screen.showFullScreen()
                QTimer.singleShot(30000, self.finish_countdown)
                
                from music import music_player
                QTimer.singleShot(30000, music_player.play_random_music)
                self.photon_network.send_start_signal()

                self.tab_ind = 33
                QApplication.processEvents()
                
        elif index == 34:  # F7
            print("Change IP")
            self.show_ip_input_dialog()
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 34
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(34, 0))            
        elif index == 35:  # F8
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            self.tab_ind = 35
            QApplication.processEvents()
            QTimer.singleShot(0, lambda: self.tab_to_target_red(35, 0))           
        elif index == 36:  # F10
            for row_index, row in enumerate(self.red_row): 
                    row[1].setStyleSheet("color: black;")
            for row_index, row in enumerate(self.green_row):  
                    row[1].setStyleSheet("color: black;")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(36, 0))
            self.tab_ind = 36   
            QApplication.processEvents()           
        elif index == 37:  # F12
            self.clear_all_players()  
    
    def is_valid_ip(self, ip):
         """Check if the given string is a valid IPv4 address."""
         try:
             socket.inet_aton(ip)
             return True
         except socket.error:
             return False
 
     
    def show_ip_input_dialog(self):
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
         confirm_button.clicked.connect(lambda: self.update_server_ip(popup, ip_input.text()))
         button_layout.addWidget(confirm_button)
 
         layout.addLayout(button_layout)
         popup.setLayout(layout)
         popup.exec()
 
    def update_server_ip(self, popup, new_ip):
         new_ip = ".".join(["0"] * (3 - new_ip.count(".")) + new_ip.split("."))
         if not self.is_valid_ip(new_ip.strip()):
             print("Invalid IP address entered.")
             error_popup = QDialog(self)
             error_popup.setWindowTitle("Error")
             error_popup.setModal(True)
             error_popup.setStyleSheet("background-color: black; color: white;")
             error_popup.resize(250, 100)
 
             layout = QVBoxLayout()
             error_label = QLabel("Invalid IP Address. Try again.")
             layout.addWidget(error_label)
 
             close_button = QPushButton("OK")
             close_button.clicked.connect(error_popup.close)
             layout.addWidget(close_button)
 
             error_popup.setLayout(layout)
             error_popup.exec()
             return  # Stop execution if IP is invalid
 
         popup.close()  # Close the input popup if valid
         self.photon_network.server_ip = new_ip.strip()
         self.photon_network.client_ip = new_ip.strip()
         print("changed to ", new_ip.strip())
         if PlayerEntryScreen.photon_network_instance:
            print("Closing existing network instance...")
            PlayerEntryScreen.photon_network_instance.close()
            
            time.sleep(1) 

         try:
            server.server_instance.restart_server(new_ip.strip())
            PlayerEntryScreen.photon_network_instance = PhotonNetwork(
            server_ip=new_ip, server_port=7500, client_port=7501
            )

            self.photon_network = PlayerEntryScreen.photon_network_instance 
            print(f"Successfully changed server IP to {new_ip}")
            self.photon_network.update_ip(new_ip)

         except socket.error as e:
            print(f"Error binding to new IP {new_ip}: {e}")

         #self.photon_network.update_ip(new_ip.strip())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    self = PlayerEntryScreen()
    self.show()
    QMetaObject.invokeMethod(self.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection)
    timer = QTimer()
    timer.timeout.connect(self.toggle_visibility)
    timer.start(100)

    sys.exit(app.exec())
