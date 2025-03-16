import socket
import threading

def start_server(server_ip="127.0.0.1", server_port=7500, client_port=7501):
    """Start the UDP server."""
    buffer_size = 1024

    server_ip = "127.0.0.1"

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

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

def update_ip(self, new_ip):
        """Updates the server IP and restarts the socket."""
        self.running = False  # Stop the old loop
        if self.server_socket:
            self.server_socket.close()
        self.server_ip = new_ip.strip()
        self.running = True  # Restart the loop
        print(f"Server IP changed to: {self.server_ip}")
        threading.Thread(target=self.start_server, daemon=True).start()

# Example usage
if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Keep the main thread alive to keep the server running
    server_thread.join()
