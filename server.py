import socket
import threading

class Server:
    def __init__(self, server_ip="127.0.0.1", server_port=7500, client_port=7501):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_port = client_port
        self.server_socket = None
        self.running = False
        self.thread = None

    def start_server(self):
        """Start the UDP server using the instance's IP and port."""
        if self.running:
            print("⚠ Server is already running!")
            return

        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.server_socket.bind((self.server_ip, self.server_port))
            print(f"✅ Server listening on {self.server_ip}:{self.server_port}")
        except OSError as e:
            print(f"❌ Error: {e}")
            self.running = False
            return

        while self.running:
            try:
                data, client_address = self.server_socket.recvfrom(1024)
                message = data.decode('utf-8')

                if message == "202":
                    response = "202"
                else:
                    response = f"{message}"

                self.server_socket.sendto(response.encode('utf-8'), (client_address[0], self.client_port))

            except socket.error:
                break  # Exit loop if socket is closed

    def stop_server(self):
        """Stop the server properly."""
        if self.running:
            self.running = False
            if self.server_socket:
                self.server_socket.close()
            print("❌ Server stopped.")

    def restart_server(self, new_ip):
        """Restart the server with a new IP."""
        print(f"🔄 Restarting server with new IP: {new_ip}...")

        self.stop_server()  # ✅ Stop the existing server first
        self.server_ip = new_ip.strip()
        self.thread = threading.Thread(target=self.start_server, daemon=True)
        self.thread.start()

# ✅ Create a global `server_instance`
server_instance = Server()

# Example usage
if __name__ == "__main__":
    server_instance.start_server()
