import os
import socket
import json
import random

class Peer:
    def __init__(self, tracker_host, tracker_port, shared_directory):
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port
        self.shared_directory = shared_directory
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)  # Set a timeout of 5 seconds
        try:
            self.client_socket.connect((self.tracker_host, self.tracker_port))
        except Exception as e:
            print("Error connecting to tracker:", e)

    def send_message(self, message):
        try:
            print("Sending message:", message)  # Add this line for debugging
            self.client_socket.sendall(json.dumps(message).encode())
            response = self.client_socket.recv(1024)
            print("Received response:", response)  # Add this line for debugging
            return json.loads(response.decode())
        except socket.timeout:
            print("Socket operation timed out.")
            return {'status': 'error', 'message': 'Socket operation timed out.'}
        except Exception as e:
            print("Error:", e)
            return {'status': 'error', 'message': str(e)}

    def register(self, user_name, password):
        message = {'action': 'register', 'user_name': user_name, 'password': password}
        register_response = self.send_message(message)

        if register_response['status'] == 'success':
            # Create a new directory for the peer in the shared_directory
            peer_directory = os.path.join(self.shared_directory, f"Peer{user_name}")
            os.makedirs(peer_directory, exist_ok=True)

            # Add dummy files to the peer's directory
            for i in range(2):
                with open(os.path.join(peer_directory, f"file{i}.txt"), 'w') as f:
                    f.write(f"Dummy file {i} for Peer{user_name}")

        return register_response

    def login(self, user_name, password):
        message = {'action': 'login', 'user_name': user_name, 'password': password}
        login_response = self.send_message(message)
        token_id = login_response.get('token_id', None)  # Extract token ID from login response
        return token_id

    def logout(self, token_id):
        message = {'action': 'logout', 'token_id': token_id}
        logout_response = self.send_message(message)
        return logout_response

    def list(self):
        message = {'action': 'list'}
        response = self.send_message(message)

        if 'status' in response and response['status'] == 'success':
            files = response['files']
        else:
            files = []

        return files


    def details(self, filename):
        message = {'action': 'details', 'filename': filename}
        return self.send_message(message)

    def __del__(self):
        self.client_socket.close()  # Close the socket when Peer instance is deleted

if __name__ == "__main__":
    shared_directory = "/home/kafka/p2p/src/shared_directory"
    peer = Peer("localhost", 5000, shared_directory)  # Host and port of the Tracker

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. List available files")
        print("5. Get details of a file")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("\nEnter username: ")
            password = input("\nEnter password: ")
            register_response = peer.register(username, password)
            print(register_response,"\n")

        elif choice == "2":
            username = input("\nEnter username: ")
            password = input("\nEnter password: ")
            login_response = peer.login(username, password)
            print("\nYour connection's ID is:",login_response,"\n")

        elif choice == "3":
            # Assuming you need to provide the token ID for logout
            token_id = input("\nEnter your token ID: ")
            logout_response = peer.logout(token_id)
            print(logout_response,"\n")

        elif choice == "4":
            list_response = peer.list()
            print(list_response,"\n")

        elif choice == "5":
            filename = input("\nEnter filename: ")
            details_response = peer.details(filename)
            print(details_response,"\n")

        elif choice == "6":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice. Please try again.")
