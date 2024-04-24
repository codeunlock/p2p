import socket
import threading
import json
import random
import os
class Tracker:
    def __init__(self, port,shared_directory):
        self.port = port
        self.peers = {}  # Stores info about the connected peers
        self.files = {}  # Stores info about the available files
        self.connected_ids = []  # List to store currently connected token IDs
        self.shared_directory = shared_directory

    def handle_peer(self, connection, address):
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            self.process_message(message, connection, address)
        connection.close()

    # Type of messages
    def process_message(self, message, connection, address):
        action = message.get('action')
        if action == 'register':
            self.register(message, connection, address)
        elif action == 'login':
            self.login(message, connection, address)
        elif action == 'logout':
            self.logout(message, connection)
        elif action == 'list':
            self.reply_list(connection)
        elif action == 'details':
            self.reply_details(message, connection)
        elif action == 'add_file':
            self.add_file(message, connection)

    # Registration function
    def register(self, message, connection, address):
        user_name = message.get("user_name")
        password = message.get("password")  # Extract password from message
        if user_name in self.peers:
            response = {'status': 'error', 'message': 'Username already exists'}
        else:
            self.peers[user_name] = {'password': password, 'address': address}  # Store password along with user info
            response = {'status': 'success', 'message': 'Registration successful'}
        connection.sendall(json.dumps(response).encode())

    def login(self, message, connection, address):
        user_name = message.get("user_name")
        password = message.get("password")

        if user_name in self.peers:
            if 'token_id' in self.peers[user_name]:  # Check if user already has a token ID
                response = {'status': 'error', 'message': 'User is already logged in'}
            elif self.peers[user_name]['password'] == password:
                token_id = random.randint(1, 1000)
                print("New Connection's Token ID:", token_id)
                self.peers[user_name]['token_id'] = token_id
                self.connected_ids.append(token_id)
                print("Connected IDs:", self.connected_ids)  # Checking if id is added correctly
                response = {'status': 'success', 'token_id': token_id}
            else:
                response = {'status': 'error', 'message': 'Incorrect password'}
        else:
            response = {'status': 'error', 'message': 'Username not foundshared_directory'}

        connection.sendall(json.dumps(response).encode())
        return response


    # logout function
    def logout(self, message, connection):
        token_id = int(message.get('token_id'))  # Convert to integer
        print("Token ID to logout:", token_id)
        print("Connected IDs before logout:", self.connected_ids)

        if token_id in self.connected_ids:
            self.connected_ids.remove(token_id)
            print("Connected IDs after logout:", self.connected_ids)

            for user_name, peer_info in self.peers.items():
                if peer_info.get('token_id') == token_id:
                    del self.peers[user_name]['token_id']
                    print(f"Token ID {token_id} removed for user {user_name}")

            response = {'status': 'success', 'message': 'Logout successful'}
            connection.sendall(json.dumps(response).encode())  # Send the response back to the peer
        else:
            print("Token ID not found in connected IDs list")
            response = {'status': 'error', 'message': 'Token ID not found in connected IDs list'}
            connection.sendall(json.dumps(response).encode())  # Send the error response back to the peer

        print("Logout response:", response)  # Add this line for debugging
        return response

    def reply_list(self, connection):
        try:
            files = []
            for root, dirs, filenames in os.walk(self.shared_directory):
                print("Root:", root)
                print("Directories:", dirs)
                print("Filenames:", filenames)
                for dir_name in dirs:
                    if dir_name.startswith("Peer"):
                        peer_directory = os.path.join(root, dir_name)
                        print("Peer directory:", peer_directory)
                        peer_files = [f for f in os.listdir(peer_directory) if f.endswith('.txt')]
                        print("Peer files:", peer_files)
                        files.extend(peer_files)

            response = {'status': 'success', 'files': files}
            connection.sendall(json.dumps(response).encode())
            print("List response sent successfully.")
        except Exception as e:
            print("Error listing files:", e)
            response = {'status': 'error', 'message': 'Error listing files'}
            connection.sendall(json.dumps(response).encode())

    def reply_details(self, message, connection):
        filename = message.get('filename')
        print("Tracker records:", self.files)  # Add this line to print the tracker's records
        if filename in self.files:
            details = self.files[filename]
            connection.sendall(json.dumps(details).encode())
        else:
            response = {'status': 'error', 'message': 'File not found'}
            connection.sendall(json.dumps(response).encode())


    def add_file(self, message, connection):
        filename = message.get('filename')
        file_details = message.get('file_details')
        self.files[filename] = file_details
        response = {'status': 'success', 'message': f'File {filename} added successfully'}
        connection.sendall(json.dumps(response).encode())

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', self.port))
            server_socket.listen()
            print(f"Tracker is listening on port {self.port}...")

            while True:
                connection, address = server_socket.accept()
                print(f"Connected to {address}")
                thread = threading.Thread(target=self.handle_peer, args=(connection, address))
                thread.start()

if __name__ == "__main__":
    shared_directory = "/home/kafka/p2p/src/shared_directory/"
    tracker = Tracker(5000,shared_directory)  # Port number
    tracker.start()
