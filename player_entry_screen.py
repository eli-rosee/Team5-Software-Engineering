from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QGridLayout,QLineEdit,QSizePolicy, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer,QMetaObject,QEvent
from functools import partial
import sys
import keyboard



def on_key_event(event):
    #print(f"Key pressed: {event.name}")
    if (event.name=="f3"):
        print("Start game")
    elif(event.name=="f1"):
        print("Back to loading screen")
    elif(event.name=="tab"):
        #main_window.change_tab_ind()
        QTimer.singleShot(0, main_window.change_tab_ind)  
        #print(main_window.tab_ind)
    elif(event.name=="esc"):
        QMetaObject.invokeMethod(main_window.timer, "stop", Qt.ConnectionType.QueuedConnection)
        QMetaObject.invokeMethod(QApplication.instance(), "quit", Qt.ConnectionType.QueuedConnection)
    elif(event.name=="enter"):
        #print("test")
        if not main_window.popup_active:  
            QTimer.singleShot(0, main_window.add_player_by_key)
    else:  
        if(1==2):
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


        self.red_team_layout.addLayout(self.red_team_info_layout)

        
        self.red_team_list = QGridLayout()
        self.red_row = []
        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field2.setReadOnly(True)
            """
            if (i != 0):
                input_field1.setReadOnly(True)
                input_field2.setReadOnly(True)
                
            input_field1.setReadOnly(True)
            """
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            QApplication.setStyle("windows")  
            checkbox.setStyleSheet("color: white; margin-left: 5px;")

            self.red_row.append((checkbox, arrow_label, num_label, input_field1, input_field2))
            self.red_team_list.addWidget(arrow_label, i, 1)
            self.red_team_list.addWidget(checkbox, i, 0)
            self.red_team_list.addWidget(num_label, i, 2)
            self.red_team_list.addWidget(input_field1, i, 3)
            self.red_team_list.addWidget(input_field2, i, 4)
            #input_field2.textChanged.connect(self.check_inputs)
            # Connect stateChanged with partial to pass the checkbox itself
            field=input_field1
            field2=input_field2 
            player_num=i
            team="Red"
            checkbox.stateChanged.connect(
                partial(self.on_checkbox_toggled, checkbox, field, field2, player_num, team)
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

        self.green_team_layout.addLayout(self.green_team_info_layout)
        
        self.green_team_list = QGridLayout()
        self.green_row = []
        for i in range(15):
            num_label = QLabel(f"{i}")
            num_label.setStyleSheet("color: white;")
            input_field1 = QLineEdit()
            input_field2 = QLineEdit()
            input_field1.setStyleSheet("background-color: white; color: black;")
            input_field2.setStyleSheet("background-color: white; color: black;")
            input_field2.setReadOnly(True)
            """
            if (i != 0):
                input_field1.setReadOnly(True)
                input_field2.setReadOnly(True)
                
            input_field1.setReadOnly(True)
            """
            arrow_label = QLabel(">>")  
            arrow_label.setStyleSheet("font-weight: bold; color: black;")
            checkbox = QCheckBox()
            QApplication.setStyle("windows")  
            checkbox.setStyleSheet("color: white; margin-left: 5px;")
            self.green_row.append((checkbox, arrow_label, num_label, input_field1, input_field2))
            self.green_team_list.addWidget(checkbox, i, 0)
            self.green_team_list.addWidget(arrow_label, i, 1)
            self.green_team_list.addWidget(num_label, i, 2)
            self.green_team_list.addWidget(input_field1, i, 3)
            self.green_team_list.addWidget(input_field2, i, 4)
            #input_field2.textChanged.connect(self.check_inputs)
            field=input_field1
            field2=input_field2 
            player_num=i
            team="Green"
            checkbox.stateChanged.connect(
                partial(self.on_checkbox_toggled, checkbox, field, field2, player_num, team)
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
        if main_window.tab_ind >= 30:
            return

        team = "Red" if main_window.tab_ind % 2 == 0 else "Green"
        row_index = main_window.tab_ind // 2  

        if team == "Red":
            row = main_window.red_row[row_index]
        else:
            row = main_window.green_row[row_index]

        checkbox, arrow_label, num_label, player_id_field, code_name_field = row
        self.on_checkbox_toggled(
            checkbox,  # Checkbox for this row
            player_id_field,  # Player ID input field
            code_name_field,  # Code Name input field
            row_index,  # The row index
            team,  
            Qt.CheckState.Checked  
        )
        checkbox.setCheckState(Qt.CheckState.Checked) 
        if (code_name_field.text() != ""):
            QTimer.singleShot(0, main_window.change_tab_ind)      
        
    def change_tab_ind(self):
                main_window.tab_ind += 1
                if (main_window.tab_ind == 38):
                    main_window.tab_ind = 0

                if (main_window.tab_ind < 30):
                    if (main_window.tab_ind%2==0):
                        if(self.red_row[(main_window.tab_ind) // 2][3].text() == ""):
                            target_input = self.red_row[(main_window.tab_ind) // 2][3]
                        else:
                             target_input = self.red_row[(main_window.tab_ind) // 2][4]
                        target_input.setFocus()  
                        #print(target_input)
                        QMetaObject.invokeMethod(target_input, "setFocus", Qt.ConnectionType.QueuedConnection)
                    elif(main_window.tab_ind%2==1):
                        if(self.green_row[(main_window.tab_ind) // 2][3].text() == ""):
                            target_input = self.green_row[(main_window.tab_ind) // 2][3]
                        else:
                             target_input = self.green_row[(main_window.tab_ind) // 2][4]
                        target_input.setFocus()  
                        #print(target_input)
                        QMetaObject.invokeMethod(target_input, "setFocus", Qt.ConnectionType.QueuedConnection)


                for button in self.buttons.values():
                    button.setStyleSheet("background-color: white; color: green; font-size: 12px;")

                if main_window.tab_ind in self.buttons:
                    button = self.buttons[main_window.tab_ind]

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
            
            for index, (arrow_label, checkbox, num_label, input1, input2) in enumerate(combined_rows):
                row_index = int(num_label.text()) if num_label.text() else index  

                if main_window.tab_ind % 2 == 0:

                    if (main_window.tab_ind // 2) < len(self.red_row):
                        self.red_row[main_window.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if ((main_window.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[(main_window.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: black;")

                elif main_window.tab_ind % 2 == 1:

                    if ((main_window.tab_ind - 1) // 2) < len(self.green_row):
                        self.green_row[(main_window.tab_ind - 1) // 2][1].setStyleSheet("font-weight: bold; color: white;")
                    
                    if (main_window.tab_ind // 2) < len(self.red_row):
                        self.red_row[main_window.tab_ind // 2][1].setStyleSheet("font-weight: bold; color: black;")

                else:
                    if index // 2 < len(self.red_row):
                        self.red_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")
                    if index // 2 < len(self.green_row):
                        self.green_row[index // 2][1].setStyleSheet("font-weight: bold; color: black;")

    def sort_players(self):
            for i in range(len(self.red_row) - 1):
                checkbox, arrow_label, num_label, player_id_field, code_name_field = self.red_row[i]

                if player_id_field.text().strip() == "" and code_name_field.text().strip() == "":
                    for j in range(i + 1, len(self.red_row)):
                        next_checkbox, next_arrow, next_num, next_player_id, next_code_name = self.red_row[j]

                        if next_player_id.text().strip() != "" or next_code_name.text().strip() != "":
                            QTimer.singleShot(0, main_window.change_tab_ind) 
                            player_id_field.setText(next_player_id.text())
                            player_id_field.setReadOnly(True)
                            code_name_field.setText(next_code_name.text())
                            code_name_field.setReadOnly(True)

                            next_player_id.clear()
                            next_player_id.setReadOnly(False)
                            next_code_name.clear()
                            next_code_name.setReadOnly(True)

                            checkbox.setChecked(True)
                            checkbox.setCheckState(Qt.CheckState.Checked)
                            next_checkbox.setChecked(False)
                            next_checkbox.setCheckState(Qt.CheckState.Unchecked)
                            next_checkbox.setEnabled(True)
                            
                            break 
            for i in range(len(self.green_row) - 1):
                checkbox, arrow_label, num_label, player_id_field, code_name_field = self.green_row[i]

                if player_id_field.text().strip() == "" and code_name_field.text().strip() == "":
                    for j in range(i + 1, len(self.green_row)):
                        next_checkbox, next_arrow, next_num, next_player_id, next_code_name = self.green_row[j]

                        if next_player_id.text().strip() != "" or next_code_name.text().strip() != "":
                            QTimer.singleShot(0, main_window.change_tab_ind) 
                            player_id_field.setText(next_player_id.text())
                            player_id_field.setReadOnly(True)
                            code_name_field.setText(next_code_name.text())
                            code_name_field.setReadOnly(True)

                            next_player_id.clear()
                            next_player_id.setReadOnly(False)
                            next_code_name.clear()
                            next_code_name.setReadOnly(True)

                            checkbox.setChecked(True)
                            checkbox.setCheckState(Qt.CheckState.Checked)
                            next_checkbox.setChecked(False)
                            next_checkbox.setCheckState(Qt.CheckState.Unchecked)


                            
                            break 

    def on_checkbox_toggled(self, checkbox, field, field2, player_num, team, state):
        player_id = field.text().strip()
        code_name = field2.text().strip()

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
                field.setReadOnly(True)
                self.directions.setText(f"Enter {player_id}'s CODE NAME:")
                QMetaObject.invokeMethod(field2, "setFocus", Qt.ConnectionType.QueuedConnection)
                field2.setReadOnly(False)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                return

        checkbox.setEnabled(False)
        self.sort_players()
        field2.setReadOnly(True)
        #QTimer.singleShot(0, main_window.change_tab_ind) 

        if not self.popup_active:  
            self.show_popup_input(player_id, code_name)

        self.popup_active = False
        self.directions.setText("Enter a NEW PLAYER ID:")    

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
            if equipment_id.strip() == "":
                return

            popup.accept()  

    def install_input_event_listeners(self):
            for row in self.red_row + self.green_row: 
                row[3].installEventFilter(self)  
                row[4].installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if isinstance(obj, QLineEdit):  
                for row_index, row in enumerate(self.red_row):  
                    row[1].setText("")
                    if obj in (row[3], row[4]):  
                        row[1].setText(">>")
                        self.tab_to_target_red(row_index * 2)
                        return True
                
                for row_index, row in enumerate(self.green_row):  
                    row[1].setText(">>")
                    if obj in (row[3], row[4]):  
                        self.tab_to_target_green(row_index * 2 + 1)
                        return True  

        return super().eventFilter(obj, event)  
    

    def tab_to_target_red(self, target_index, extra_steps=0):
        if main_window.tab_ind != target_index or extra_steps > 0:
            self.change_tab_ind()  

            if extra_steps > 0:
                extra_steps -= 1  
            
            QTimer.singleShot(0, lambda: self.tab_to_target_red(target_index, extra_steps))  


    def tab_to_target_green(self, target_index, extra_steps=0):
        if main_window.tab_ind != target_index or extra_steps > 0:
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
            QTimer.singleShot(0, lambda: self.tab_to_target_red(30, 0))  
        elif index == 31:  # F2 Game Parameters
            print("Adjusting Game Parameters...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(31, 0)) 
        elif index == 32:  # F3 Start Game
            print("Starting Game...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(32, 0)) 
        elif index == 33:  # F5 PreEntered Games
            print("Viewing PreEntered Games...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(33, 0)) 
        elif index == 34:  # F7
            print("F7 Action Triggered")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(34, 0))             
        elif index == 35:  # F8 View Game
            print("Viewing Game...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(35, 0))             
        elif index == 36:  # F10 Flick Sync
            print("Performing Flick Sync...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(36, 0))             
        elif index == 37:  # F12 Clear Game
            print("Clearing Game...")
            QTimer.singleShot(0, lambda: self.tab_to_target_red(37, 0))             

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PlayerEntryScreen()
    main_window.show()
    QMetaObject.invokeMethod(main_window.red_row[0][3], "setFocus", Qt.ConnectionType.QueuedConnection)
    keyboard.on_press(on_key_event)
    timer = QTimer()
    timer.timeout.connect(main_window.toggle_visibility)
    timer.start(100)

    sys.exit(app.exec())
