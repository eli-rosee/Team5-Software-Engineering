import socket
import threading

class Server:
    def __init__(self, server_ip="127.0.0.1"):
        self.server_ip = server_ip
        self.receive_port = 7501  
        self.broadcast_port = 7500 
        self.running = False
        self.receive_socket = None
        self.broadcast_socket = None
        self.thread = None

    def start_server(self):
        self.running = True
        buffer_size = 1024

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind((self.server_ip, self.receive_port))
        self.receive_socket.settimeout(1.0) 

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print(f"Server listening on {self.server_ip}:{self.receive_port}")

        try:
            while self.running:
                try:
                    data, client_address = self.receive_socket.recvfrom(buffer_size)
                    message = data.decode('utf-8')
                    print(f"Received: {message} from {client_address}")

                    if ":" in message:
                        parts = message.split(":")
                        if len(parts) == 2:
                            attacker, code = parts
                            if code in ("43", "53"):
                                response = attacker
                            else:
                                response = code
                        else:
                            response = message
                    else:
                        response = message

                    self.broadcast_socket.sendto(response.encode('utf-8'), (self.server_ip, self.broadcast_port))
                except socket.timeout:
                    continue  # keep server alive if no data received
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop_server()

    def stop_server(self):
        self.running = False
        if self.receive_socket:
            self.receive_socket.close()
            self.receive_socket = None
        if self.broadcast_socket:
            self.broadcast_socket.close()
            self.broadcast_socket = None
        print("Server stopped.")


    def run_in_thread(self):
        self.thread = threading.Thread(target=self.start_server, daemon=True)
        self.thread.start()

    def restart_server(self, new_ip):
        self.stop_server()  # Clean up old sockets
        self.server_ip = new_ip.strip()
        self.run_in_thread()


def start_server_in_thread():
    """ Function to start the server in a separate thread """
    try:
        server_instance.start_server()
    except Exception as e:
        print(f"Error starting server: {e}")

server_instance = Server()
def get_instance():
    return server_instance
if __name__ == "__main__":

    server_thread = threading.Thread(target=start_server_in_thread, daemon=True)
    server_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server_instance.stop_server()
