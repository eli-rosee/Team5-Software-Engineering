import socket
import threading
import time

class PhotonNetwork:
    def __init__(self, server_ip="127.0.0.1", server_port=7500, client_port=7501):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.serverAddressPort = (server_ip, server_port)

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.settimeout(1)

        self._running = True
        self.receive_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
        self.receive_thread.start()

    def send_start_signal(self):
        """Send start signal to server on port 7500"""
        self.broadcast_socket.sendto(b"202", self.serverAddressPort)

    def send_stop_signal(self):
        """Send stop signal to server"""
        stop_msg = b"221"
        for _ in range(3):
            self.broadcast_socket.sendto(stop_msg, self.serverAddressPort)

    def equipID(self, equip_id):
        """Send equipment ID to server (tagged player only)"""
        message = equip_id.encode()
        self.broadcast_socket.sendto(message, self.serverAddressPort)

    def listen_for_responses(self):
        """Listen for server responses on any source (no bind)"""
        while self._running:
            try:
                data, _ = self.receive_socket.recvfrom(1024)
                print(f"Received: {data.decode('utf-8')}")
            except socket.timeout:
                continue
            except OSError as e:
                if not self._running:
                    break  # Graceful exit
                print(f"Receive error: {e}")
                break

    def close(self):
        self._running = False

        if self.broadcast_socket:
            self.broadcast_socket.close()
            self.broadcast_socket = None

        if self.receive_socket:
            self.receive_socket.close()
            self.receive_socket = None

        print("Closed PhotonNetwork sockets.")

    def update_ip(self, new_ip):
        self.server_ip = new_ip.strip()
        self.serverAddressPort = (self.server_ip, self.server_port)
