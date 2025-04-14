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
    def start_server(server_ip="127.0.0.1", server_port=7500, client_port=7501):
        """Start the UDP server."""
        buffer_size = 1024

        server_ip = "127.0.0.1"

        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((server_ip, client_port))

        print(f"Server listening on {server_ip}:{server_port}")

        while True:
            # Receive data from the client
            data, client_address = server_socket.recvfrom(buffer_size)
            message = data.decode('utf-8')

            if message == "202":
                # Start signal, no need to handle equip ID
                response = "202"
            else:
                # Assume the message is an equipment ID
                response = f"{message}"

            # Send the response back to the client
            server_socket.sendto(response.encode('utf-8'), (client_address[0], client_port))

    def stop_server(self):
            """Stop the server properly."""
            self.running = False
            if self.server_socket:
                self.server_socket.close()

    def update_ip(self, new_ip):
            """Change the server's IP and restart the server."""
            self.stop_server()
            self.server_ip = new_ip.strip()
            print(f"Server IP changed to: {self.server_ip}")
            threading.Thread(target=self.start_server, daemon=True).start()

    def restart_server(self, new_ip):
            """Restart the server with a new IP."""
            self.stop_server()
            self.server_ip = new_ip.strip()
            self.thread = threading.Thread(target=self.start_server, daemon=True)
            self.thread.start()

server_instance = Server()

# Example usage
if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=Server.start_server, daemon=True)
    server_thread.start()

    # Keep the main thread alive to keep the server running
    server_thread.join()
