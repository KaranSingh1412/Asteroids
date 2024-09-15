import socket

# Die Klasse AsteroidsServer ist für die Kommunikation zwischen dem Server und dem Client verantwortlich.
class AsteroidsServer:
    # Konstruktor der AsteroidsServerklasse
    def __init__(self):
        self.TCP_IP = '0.0.0.0' # IP-Adresse des Servers
        self.TCP_PORT = 12345 # Port des Servers
        self.hasConnection = False
        self.connectedClient = None
        self.received_data = None
        self.client_socket = None # Socket des Clients
        self.running = False

    def get_local_ip(self):
        try:
            # Erstellen Sie einen temporären UDP Socket, um die lokale IP-Adresse zu ermitteln
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
        
    def start_server(self):
        # Erstellen Sie einen TCP-Socket und binden Sie ihn an die IP-Adresse und den Port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.TCP_IP, self.TCP_PORT))
        server_socket.listen(1)
        server_socket.settimeout(1.0)  # Timeout für accept()
        print(f"Server listening on {self.TCP_IP}:{self.TCP_PORT}")
        self.running = True

        while self.running:
            try:
                # Warten auf eine eingehende Verbindung
                self.client_socket, addr = server_socket.accept()
                print(f"Connected by {addr}")
                self.hasConnection = True
                self.connectedClient = addr
                # Setzen Sie einen kleinen Timeout für recv()
                self.client_socket.settimeout(0.1)
                self.handle_client()
            except socket.timeout:
                continue

        server_socket.close()

    # Empfangen und Senden von Daten vom Client
    def handle_client(self):
        while self.running and self.hasConnection:
            try:
                # Empfangen von Daten vom Client (maximal 1024 Bytes)
                data = self.client_socket.recv(1024)
                if not data:
                    self.hasConnection = False
                    break
                self.received_data = data.decode('utf-8') # Dekodieren der empfangenen Daten in ein lesbares Format
                print(f"Received: {self.received_data}")
            except socket.timeout:
                continue
            except:
                self.hasConnection = False
                break

        if self.client_socket:
            self.client_socket.close()

    # Senden eines Signals an den Client
    def send_signal(self, signal):
        if self.hasConnection and self.client_socket:
            try:
                # Senden des Signals an den Client
                self.client_socket.sendall(signal.encode('utf-8'))
                print(f"Sent signal: {signal}")
            except:
                # Fehler beim Senden des Signals
                print("Failed to send signal")
                self.hasConnection = False

    def stop_server(self):
        # Stoppen des Servers und Schließen des Sockets
        self.running = False
        print("Server stopped")
        if self.client_socket:
            self.client_socket.close()