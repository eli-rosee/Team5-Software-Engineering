DB_NAME = "laser_tag"
DB_USER = "laser_admin"
DB_PASSWORD = "student"  
DB_HOST = "127.0.0.1"
DB_PORT = "5432"  # PostgreSQL default port

def connect():
    """Establish a connection to the PostgreSQL database."""
    print("Attempting to connect to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to PostgreSQL successfully!")
        return conn
    except psycopg2.Error as e:
        print("Database connection failed:", e)
        return None

def get_player_by_id(player_id):
    """Check if a player exists in the database by player ID."""
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT codename FROM players WHERE player_id = %s;", (player_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None  # Return codename if found, otherwise None
    return None

def add_new_player(player_id, codename, equipment_id, team):
    """Insert a new player into the database."""
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO players (player_id, codename, equipment_id, team) VALUES (%s, %s, %s, %s);",
            (player_id, codename, equipment_id, team),
        )
        conn.commit()
        cursor.close()
        conn.close()
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

# Player Entry via Terminal Input
if __name__ == "__main__":
    print("\n--- Add Two Players ---")

    for i in range(2):  # Loop to add two players
        while True:
            try:
                player_id = int(input(f"\nEnter Player {i+1} ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer for Player ID.")

        codename = input(f"Enter Player {i+1} Codename: ")

        while True:
            try:
                equipment_id = int(input(f"Enter Player {i+1} Equipment ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer for Equipment ID.")

        while True:
            team = input(f"Enter Player {i+1} Team (red/green): ").strip().lower()
            if team in ["red", "green"]:
                break
            print("Invalid input. Team must be 'red' or 'green'.")

        # Check if player already exists
        existing_player = get_player_by_id(player_id)
        if existing_player:
            print(f"Player {player_id} already exists with codename: {existing_player}")
        else:
            add_new_player(player_id, codename, equipment_id, team)

    # Show all players after addition
    print("\nAll Players in Database:")
    for p in get_all_players():
        print(p)
