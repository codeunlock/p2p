import socket
import threading
import json

class Tracker:
    def __init__(self, port):
        self.port = port
        self.peers = {}  # Dictionary to store information about registered peers
        self.files = {}  # Dictionary to store information about shared files
        self.lock = threading.Lock()  # Lock for thread-safe access to peer and file data

    def handle_peer(self, connection, address):
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            self.process_message(message, connection, address)
        connection.close()

    def process_message(self, message, connection, address):
        action = message.get('action')
        if action == 'register':
            self.register_peer(message, connection, address)
        elif action == 'login':
            self.login_peer(message, connection, address)
        elif action == 'logout':
            self.logout_peer(message)
        elif action == 'list':
            self.send_file_list(connection)
        elif action == 'details':
            self.send_file_details(message, connection)
        # Add more actions as needed

    def register_peer(self, message, connection, address):
        username = message.get('username')
        if username in self.peers:
            response = {'status': 'error', 'message': 'Username already exists'}
        else:
            self.peers[username] = {'address': address}
            response = {'status': 'success', 'message': 'Registration successful'}
        connection.sendall(json.dumps(response).encode())

    def login_peer(self, message, connection, address):
        username = message.get('username')
        if username in self.peers:
            # Check password (not implemented in this simplified version)
            token_id = username  # For simplicity, use username as token_id
            self.peers[username]['token_id'] = token_id
            response = {'status': 'success', 'token_id': token_id}
        else:
            response = {'status': 'error', 'message': 'Username not found'}
        connection.sendall(json.dumps(response).encode())

    def logout_peer(self, message):
        token_id = message.get('token_id')
        for username, peer_info in self.peers.items():
            if peer_info.get('token_id') == token_id:
                del self.peers[username]
                break

    def send_file_list(self, connection):
        files = list(self.files.keys())
        connection.sendall(json.dumps(files).encode())

    def send_file_details(self, message, connection):
        filename = message.get('filename')
        if filename in self.files:
            details = self.files[filename]
            connection.sendall(json.dumps(details).encode())
        else:
            response = {'status': 'error', 'message': 'File not found'}
            connection.sendall(json.dumps(response).encode())

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', self.port))
            server_socket.listen()

            print(f"Tracker listening on port {self.port}...")

            while True:
                connection, address = server_socket.accept()
                print(f"Connected to {address}")
                thread = threading.Thread(target=self.handle_peer, args=(connection, address))
                thread.start()

if __name__ == "__main__":
    tracker = Tracker(5000)  # Port number for the Tracker
    tracker.start()
