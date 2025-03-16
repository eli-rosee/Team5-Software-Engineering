import socket
import threading
import time

#run server then client
#works w/ player_entry_screen
#no need to use trafficgenerator it has the same functionality
class PhotonNetwork:
    def __init__(self, server_ip="127.0.0.1", server_port=7500, client_ip="127.0.0.1", client_port=7501):
        self.server_ip = server_ip  
        self.server_port = server_port
        
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

    def send_start_signal(self):
        """Send the start signal ("202") to the game software."""
        message = "202".encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)
        #print("202")

    def equipID(self, equip_id):
        """Send the equipment ID to the server."""
        message = equip_id.encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)

    def listen_for_responses(self):
        """Continuously listen for incoming data on the receive socket."""
        while self._running:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"{message}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"{e}")
                break

    def close(self):
        """Close both UDP sockets and stop the receive thread."""
        self._running = False
        self.broadcast_socket.close()
        self.receive_socket.close()
        print("Photon network connections closed.")

    def update_ip(self, new_ip):
        """Updates the server's target IP and rebinds the sockets."""
        self.server_ip = new_ip.strip()
        self.serverAddressPort = (self.server_ip, self.server_port)

        print(f"Updated server IP to: {self.server_ip}")

        # Restart sockets
        self.broadcast_socket.close()
        self.receive_socket.close()

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(self.clientAddressPort)
        self.receive_socket.settimeout(1.0)

        print("Sockets restarted with new IP.")

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
