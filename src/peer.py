import socket 
import json
#from random import randint
import random

class Peer:
     
     def __init__(self, tracker_host, tracker_port):
          self.tracker_host = tracker_host
          self.tracker_port = tracker_port

     def send_message(self, message):
          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
               client_socket.connect((self.tracker_host, self.tracker_port))
               client_socket.sendall(json.dumps(message).encode())
               response = client_socket.recv(1024) # 1024 = receiving code
               return json.loads(response.decode())
          
     def register(self, user_name, password):
          message = {'action': 'register', 'user_name': user_name, 'password': password}
          return self.send_message(message)
     
     def login(self, user_name, password):
          message = {'action': 'login', 'user_name': user_name, 'password': password}
          login_response = self.send_message(message)
          token_id = login_response.get('token_id', None)  # Extract token ID from login response
          return token_id
          
     def logout(self, token_id):
          message = {'action': 'logout', 'token_id': token_id}
          return self.send_message(message)
     
     def list(self):
          message = {'action': 'list'}
          return self.send_message(message)

     def details(self, filename):
          message = {'action': 'details', 'filenae': filename}
          return self.send_message(message)


if __name__ == "__main__":
     peer = Peer("localhost", 22222)  # Host and port of the Tracker
    
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

          elif choice == "\n4":
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

"""
TODO:
     register a new user  ~~~> DONE 
     login  ~~~> DONE 
     list available files 
     get details of a file 
     logout 
"""
