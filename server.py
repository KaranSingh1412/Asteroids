import socket

class AsteroidsServer:
    def __init__(self):
        self.TCP_IP = '0.0.0.0'
        self.TCP_PORT = 12345
        self.hasConnection = False
        self.connectedClient = None
                 

    def start_server(self):
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.TCP_IP, self.TCP_PORT))
            server_socket.listen()

            print(f"Server listening on {self.TCP_IP}:{self.TCP_PORT}")

            while True:
                # Wait for a connection
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")
                    self.hasConnection = True
                    self.connectedClient = addr
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print(f"Received: {data.decode('utf-8')}")