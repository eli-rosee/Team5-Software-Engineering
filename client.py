import socket
import threading
import time

#run server then client
#works w/ player_entry_screen
#no need to use trafficgenerator it has the same functionality
class PhotonNetwork:
    def __init__(self, server_ip="127.0.0.1", server_port=7500, client_ip="127.0.0.1", client_port=7501):
        
        self.serverAddressPort = (server_ip, server_port)
        self.clientAddressPort = (client_ip, client_port)

        # Set up the broadcast socket
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set up the receive socket
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(self.clientAddressPort)
        self.receive_socket.settimeout(1.0)  # 1-second timeout

        # Thread control
        self._running = True
        self.receive_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
        self.receive_thread.start()

        # Track added players and their equipment IDs
        self.player_equipment_map = {}  # {player_id: equipment_id}

    def send_start_signal(self):
        """Send the start signal ("202") to the game software."""
        message = "202".encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        print("Sent start signal: 202")

    def equipID(self, player_id, equip_id=None, player_name=None):
        """
        Send the player ID, equipment ID, and player name to the server.
        If equip_id and player_name are provided, send them along with the player ID.
        """
        if not isinstance(player_id, int):
            raise ValueError("player_id must be an integer")

        # Send the player ID, equipment ID, and player name to the server
        if equip_id is not None and player_name is not None:
            message = f"{player_id}:{equip_id}:{player_name}".encode()
        else:
            message = str(player_id).encode()

        self.broadcast_socket.sendto(message, self.serverAddressPort)
        print(f"Sent player ID, equipment ID, and name to server: {player_id}:{equip_id}:{player_name}")

        # Wait for the server to respond
        try:
            data, _ = self.receive_socket.recvfrom(1024)
            response = data.decode('utf-8')
            print(f"Received response from server: {response}")
        except socket.timeout:
            print(f"Timeout waiting for response from server for player {player_id}")

    def sendPlayerID(self, player_id):
        """Send a photon event with the player ID."""
        if not isinstance(player_id, int):
            raise ValueError("player_id must be an integer")
        message = str(player_id).encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        print(f"Sent photon event: {player_id}")

    def listen_for_responses(self):
        """Continuously listen for incoming data on the receive socket."""
        while self._running:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"Received from game software: {message}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def close(self):
        """Close both UDP sockets and stop the receive thread."""
        self._running = False
        self.broadcast_socket.close()
        self.receive_socket.close()
        print("Photon network connections closed.")

# Example usage
if __name__ == "__main__":
    # Start the client
    server_ip = input("Enter server IP (default is 127.0.0.1): ") or "127.0.0.1"
    photon_network = PhotonNetwork(server_ip=server_ip)

    try:
        # Send the start signal to the game software
        photon_network.send_start_signal()
        time.sleep(1)  # Wait for the game software to be ready

    except KeyboardInterrupt:
        photon_network.close()
        print("Photon network terminated.")
