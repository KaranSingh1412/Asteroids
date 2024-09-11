import socket

class AsteroidsServer:
    def __init__(self):
        self.TCP_IP = '0.0.0.0'
        self.TCP_PORT = 12345
        self.hasConnection = False
        self.connectedClient = None
        self.received_data = None
                 

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.TCP_IP, self.TCP_PORT))
        server_socket.listen()
        # Create a TCP/IP socket
        print(f"Server listening on {self.TCP_IP}:{self.TCP_PORT}")

        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        self.hasConnection = True
        self.connectedClient = addr
        while True:
            data = conn.recv(1024)
            if not data:
                break
            self.received_data = data.decode('utf-8')
            print(f"Received: {data.decode('utf-8')}")
        conn.close()