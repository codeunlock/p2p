import socket 
import json
from random import random
import os 
class Peer:
     
     def __init__(self, tracker_host, tracker_port,shared_directory):
          self.tracker_host = tracker_host
          self.tracker_port = tracker_port
          self.shared_directory = shared_directory

     def send_message(self, message):
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
               client_socket.connect((self.tracker_host, self.tracker_port))
               client_socket.sendall(json.dumps(message).encode())
               response = client_socket.recv(1024) # 1024 = receiving code
               return json.loads(response.decode())
          
     def register(self, user_name, password):
          message = {'action': 'register', 'user_name': user_name, 'password': password}
          return self.send_message(message)
     
     def login(self,user_name,password):
          message = {'action': 'login', 'user_name': user_name, 'password': password}
          return self.send_message(message)
     
     def logout(self, token_id):
          message = {'action': 'logout', 'token_id' : token_id}
          return self.send_message(message)
     
     def list(self):
          message = {'action': 'list'}
          return self.send_message(message)

     def details(self, filename):
          message = {'action': 'details', 'filenae': filename}
          return self.send_message(message)


     def register_shared_files(self):
          shared_files = os.listdir(self.shared_directory)
          for filename in shared_files:
               file_path = os.path.join(self.shared_directory, filename)
               if os.path.isfile(file_path):
                    self.register_file_with_tracker(filename)

     def register_file_with_tracker(self, filename):
          message = {'action': 'register_file', 'filename': filename}
          response = self.send_message(message)
          print(response)  # Print response from Tracker


if __name__ == "__main__":
     peer = Peer("localhost", 5000, "/Users/alex/aueb/com_net/p2p/shared_directory")  # Host and port of the Tracker
     peer.register_shared_files()
     list_response = peer.list_files()
     print(list_response)
     # Test peer registration
     register_response = peer.register("user1", "password1")
     print(register_response)

     login_respone = peer.login("user1", "password1")
     print(login_respone)

     list_response = peer.list()
     print(list_response)

""" 
TODO:
     register a new user  ~~~> DONE 
     login  ~~~> DONE 
     list available files 
     get details of a file 
     logout 
"""
