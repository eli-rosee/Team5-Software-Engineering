import socket
import threading
import time
import random

def start_server(server_ip="0.0.0.0", server_port=7500, client_port=7501):
    """Start the UDP server."""
    buffer_size = 1024

   #let user specifiy network at runtime.
    if server_ip == "0.0.0.0":
        print("Available network interfaces:")
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
        for idx, ip in enumerate(ips):
            print(f"{idx + 1}: {ip}")
        
        choice = input("Select network interface (enter number or type ip address(127.0.0.1)): ")
        if choice in ips or choice == "127.0.0.1":
            server_ip = choice
        else:
            try:
                server_ip = ips[int(choice) - 1]
            except (IndexError, ValueError):
                print("Invalid selection. Default 127.0.0.1")
                server_ip = "127.0.0.1"


    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f"Server listening on {server_ip}:{server_port}")

    # Dictionary to store player_id to (equip_id, player_name) mappings
    player_equipment_map = {}  # {player_id: (equip_id, player_name)}

    def generate_traffic():
        """Generate random traffic and send it to the client."""
        counter = 0
        while True:
            if len(player_equipment_map) >= 2:  # Start generating traffic after 2 players register
                player_ids = list(player_equipment_map.keys())
                red_player = random.choice(player_ids)
                green_player = random.choice(player_ids)

                # Look up the equipment IDs for the selected players
                red_equip_id, _ = player_equipment_map[red_player]
                green_equip_id, _ = player_equipment_map[green_player]

                # Simulate interactions between players using their equipment IDs
                if random.randint(1, 2) == 1:
                    message = f"{red_equip_id}:{green_equip_id}"
                else:
                    message = f"{green_equip_id}:{red_equip_id}"
                print(f"Generated traffic: {message}")
                server_socket.sendto(message.encode('utf-8'), ("127.0.0.1", client_port))

                # Simulate base hits after specific iterations
                if counter == 10:
                    base_hit_message = f"{red_player}:43"  # Red team base hit
                    print(f"Generated base hit: {base_hit_message}")
                    server_socket.sendto(base_hit_message.encode('utf-8'), ("127.0.0.1", client_port))
                elif counter == 20:
                    base_hit_message = f"{green_player}:53"  # Green team base hit
                    print(f"Generated base hit: {base_hit_message}")
                    server_socket.sendto(base_hit_message.encode('utf-8'), ("127.0.0.1", client_port))

                counter += 1
                time.sleep(random.randint(1, 3))  # Wait 1-3 seconds between messages

    # Start the traffic generation thread
    traffic_thread = threading.Thread(target=generate_traffic, daemon=True)
    traffic_thread.start()

    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(buffer_size)
        message = data.decode('utf-8')
        print(f"Received from client: {message}")

        if message == "202":
            # Start signal, no need to handle equip ID
            response = "202"
        elif ":" in message:
            # Handle messages in the format "player_id:equip_id:player_name"
            try:
                parts = message.split(":")
                if len(parts) == 3:
                    player_id = int(parts[0])
                    equip_id = parts[1]
                    player_name = parts[2]
                    player_equipment_map[player_id] = (equip_id, player_name)
                    print(f"Stored equip ID {equip_id} and name {player_name} for player {player_id}")
                    response = f"ACK:{player_id}:{equip_id}:{player_name}"
                else:
                    response = "Invalid message format"
            except ValueError:
                response = "Invalid player ID"
        else:
            # Assume the message is a player ID
            try:
                player_id = int(message)
                if player_id in player_equipment_map:
                    # Return the equip ID and player name for this player
                    equip_id, player_name = player_equipment_map[player_id]
                    response = f"{equip_id}:{player_name}"
                else:
                    response = "Player ID not found"
            except ValueError:
                response = "Invalid player ID"

        # Send the response back to the client
        server_socket.sendto(response.encode('utf-8'), (client_address[0], client_port))
        print(f"Sent response to client: {response}")

# Example usage
if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Keep the main thread alive to keep the server running
    server_thread.join()
