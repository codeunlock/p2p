import socket
import json

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 5000))  # Connect to Tracker on port 5000
        client_socket.sendall(json.dumps(message).encode())
        response = client_socket.recv(1024)
        print(f"Response from Tracker: {response.decode()}")

def register_peer(username, password):
    message = {'action': 'register', 'username': username, 'password': password}
    send_message(message)

def login_peer(username, password):
    message = {'action': 'login', 'username': username, 'password': password}
    send_message(message)

def logout_peer(token_id):
    message = {'action': 'logout', 'token_id': token_id}
    send_message(message)

def list_files():
    message = {'action': 'list'}
    send_message(message)

def get_file_details(filename):
    message = {'action': 'details', 'filename': filename}
    send_message(message)

if __name__ == "__main__":
    # Simulate peer interactions with the Tracker
    register_peer("user1", "password1")  # Register a new peer
    login_peer("user1", "password1")     # Login to the system
    list_files()                          # List available files
    get_file_details("/Users/alex/aueb/asps/project/src/example.txt")       # Get details of a specific file
    logout_peer("user1")                  # Logout from the system
