import psycopg2
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class Database:

    # Define constants
    DB_NAME = "photon"
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    DB_USER = "student"
    DB_PASSWORD = "student"

    # Create a new connection to the database
    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.DB_NAME,
                host=self.DB_HOST,
                user=self.DB_USER,
                password=self.DB_PASSWORD,
                port=self.DB_PORT
            )
            return conn
        except psycopg2.Error as e:
            print("Database connection failed:", e)
            return None

    # Returns the codename for the given player ID
    def get_player_by_id(self, conn, player_id):
        if conn:
            cursor = conn.cursor()
            player_id = int(player_id)
            cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None  
        return None

    # Inserts a new player into the database
    def add_new_player(self, conn, player_id, codename):
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
            conn.commit()
            cursor.close()

    # Gets all players from the database
    def get_all_players(self):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players;")
            players = cursor.fetchall()
            cursor.close()
            conn.close()
            return players  
        return []

    def enter_handler(self, field1, field2, field3, directions, tab_ind, team_red, red_row, green_row):

            player_id = field1.text().strip()
            code_name = field2.text().strip()
            equip_id = field3.text().strip()

            # Check if player_id is empty
            if not player_id:
                directions.setText("Player ID cannot be empty")
                return None

            # Make sure player_id is an integer
            try:
                int_player_id = int(player_id)
            except ValueError:
                directions.setText("Player ID must be an integer")
                return None

            # Make sure equip_id is an integer
            if equip_id:
                try:
                    int_equip_id = int(equip_id)
                except ValueError:
                    directions.setText("Equipment ID must be an integer")
                    return None
            else:
                int_equip_id = None  


            text = directions.text()
            number = text.replace("Enter ", "").replace("'s CODE NAME:", "")
        
            if "CODE NAME:" in directions.text() and field1.text() != number:
                    field1.setText("")
                    return
            elif player_id == "":
                    directions.setText("Player Does not have an ID")
                    return

            elif code_name == "" and player_id!="":
                    conn = self.connect()
                    if conn:
                            player = self.get_player_by_id(conn, player_id)
                            if player:  
                                field2.setText(player)
                                field2.setReadOnly(True)
                                directions.setText(f"Enter {player_id} equipment ID") 
                                field3.setFocus()
                                field3.setReadOnly(False)
                                QApplication.processEvents()

                                return
                            else: 
                                field2.setText("")

                            conn.close()  

                    field1.setReadOnly(True)
                    directions.setText(f"Enter {player_id}'s CODE NAME:")
                    QApplication.processEvents()
                    field2.setFocus()
                    QApplication.processEvents()
                    field2.setReadOnly(False)
                    return
            elif (equip_id=="" and code_name!="" and player_id!=""):
                    conn = self.connect()
                    if conn:
                        player = self.get_player_by_id(conn, player_id)                            
                        if player:  
                            field2.setText(player)
                        else: 
                            self.add_new_player(conn, player_id, code_name)

                    conn.close()  

                    field2.setReadOnly(True)
                    directions.setText(f"Enter {player_id} equipment ID") 
                    field3.setFocus()
                    field3.setReadOnly(False)
                    return
            else:
                directions.setText(f"Enter a NEW PLAYER ID:")
                if(tab_ind == 14 and not team_red):
                    red_row[0][2].setFocus()
                elif(team_red):
                    green_row[tab_ind][2].setFocus()
                else:
                    red_row[tab_ind + 1][2].setFocus()
