import socket
import threading
import json
from random import random 

class Tracker:
     def __init__(self, port):
          self.port = port    
          self.peers = {}  # Stores info about the connected peers
          self.files = {}  # Stores info about the available files


     def handle_peer(self, connection, address):
          while True:
               data = connection.recv(1024)
               if not data:
                    break
               message = json.loads(data.decode())
               self.process_message(message, connection, address)
          connection.close()

     # Type of messages
     def process_message(self,message,connection,address):
          action = message.get('action')
          if action == 'register':
               self.register(message, connection, address)
          elif action == 'login':
               self.login(message,connection,address)
          elif action == 'logout':
               self.logout(message)
          elif action == 'list':
               self.list(connection)
          elif action == 'details':
               self.details(message, connection)
          
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
     
     
     # Login function 
     def login(self, message, connection, address):
          user_name = message.get("user_name")
          password = message.get("password")  # Extract password from message
          if user_name in self.peers:
               if self.peers[user_name]['password'] == password:  # Check if provided password matches stored password
                    token_id = random()
                    print(token_id)  # Prints for check | TODO REMOVE IT IF CORRECT
                    response = {'status': 'success', 'token_id': token_id}
               else:
                    response = {'status': 'error', 'message': 'Incorrect password'}
          else:
               response = {'status': 'error', 'message': 'Username not found'}
          connection.sendall(json.dumps(response).encode())
     
     
     # logout function 
     def logout(self,message):
          token_id = message.get('token_id')
          for user_name, peer_info in self.peers.items():
               if peer_info.get('token_id') == token_id:
                    del self.peers[user_name]
                    break
     
     def list(self, connection):
          files = list(self.files.keys())
          connection.sendall(json.dumps(files).encode())

     def details(self, message, connection):
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
               print(f"Tracker is listening on port {self.port}...")

               while True:
                    connection, address = server_socket.accept()
                    print(f"Connected to {address}")
                    thread = threading.Thread(target = self.handle_peer, args = (connection, address))
                    thread.start()
               

if __name__ == "__main__":
    tracker = Tracker(5000)  # Port number 
    tracker.start()
