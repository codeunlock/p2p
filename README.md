#P2P File System in Python.

DATA:
System:
- 1 trackers
- multiple similar peers (6 minimum) 


Peers:
     Each peer keeps an account on the tracker.
     Each peer has a folder (shared_directory)
     Each peer after connecting with the tracker, infroms it about the files that are available
     Each peer when it wants to download, asks from tracker info(ip,port..) for this file it is interested in

Trackers & peers:
     Capable of keeping open multiple connections simultaneously 


Peer's functions:
     1) Communicate with tracker and other peers using sockers
     2) shared_directory folder
     3) Maintains a set of files. During start must already has minumum 2 files (names ~> fileDownloadList.txt)
          - Each file of the list must be saved, during start, in 2-3 peers. 
     4) Creates and maintains a tracker account(register, login, logout)
          i) register(): Peer sets username/password and sends them to tracker. If username available ~> tracker creates the account and returns success message. Else error message to peer and asks for new username.
          ii) login(): peer insterts to a message the username|password and sends it to tracker. Trackers authenticates it and create random id token_id with which it answers back.
               ~ token_id is unique and random for each session.
          Peers informs tracker for shared_directory files and communication info ip | port.
          iii) logout(): Peer informs the trackers that it logs out authenticating himself with its token_id. Trackers accepts it, return message of successfull logout and updates the data structures it maintains, appropriately about peers, and invalidates the token_id.
     5) def list():
          Peer asks the file names which are available in the P2P system from the tracker.
     6) def details():
          Peers aks from the tracker info  about a specific AVAILABLE file from the previous step (list()) by sending the name of the file.
               details() output is a list with communication info:
                    i) ip_address
                    ii) port
                    iii) user_name
                    iv) count_downloads
                    v) count_failures
                    Those info are from the peers which already have the specific file.
               or error message if file does not exist in any peer.
     7) def checkActive():
          Trackers checks if a peer, from details(), is active.
          Also must respond with confirmation message in checkActive messages it receives from other peers or from tracker.
     8) def simpleDownload(): 
          The peer when the search is done, selects the "best" peer, from the details() output and asks the file.
          
          For a peer to select the best one peer availble:
               i) sends checkActive messages in each available peer and counts the responding time for each one and 
               ii) multiplies it (for each peer) with 0.75^count_downloads*1.25^count_failures.

          - After succesfull file download, which is tested by opening the file, peers save it to the shared_directory and notifies tracker that it has the file from now on and about the user_name from which the file was sent succesfully (best one peer).
          - If the download fails it notifies the tracker about the simpleDownload() failure and also sents the user_name from the best one peer which failed. Then it selects the next one best peer (2nd for the best one selection) If there is no other available peer to donwload the file, the process is terminated and en error message is displayed to the peer that wants to download the file.
          simpleDownload() respons appopriately to request to download file from other peers.Specificaly the peer reads the requested file form its shared_directory and sends it to peer who requested it. If it does not have the file (e.g. why just its query submitted by mistake) return negative message.

Tracker's functions:
     1) Maintains appropriate data structure where it stores the info for each peer (user_name, password, count_downloads, count_failures)
     ~ count_downlaod: a simple counter, increments by one each time that the tracker gets infromed about a succesfull file transfrer from the peer with its user_name to another peer.
     ~ count_failures: Same but this time +1 whenever tracker gets informed for a failed transfer from the peer user_name.
     2) Supported functins: register, logout, login.
     3) Maintains another data structure for peers info | token_id | ip_address | port | user_name + count_downloads + count_failures.
     4) Maintains another data structure with the names of available for downlaod files. Also uses the reply_list(); see below.
     5) Data structure in which it matches each availble file to the allowed files whose names are listed in ListfileDownload.txt, in one
     list of token_ids of active peers that have them. 
     This structure is used for reply_details() (see below), At first it is empty and it is updated progressively as peers connect to the tracker and update it through the inform function.
     6) Supports multiple threads simultaneously, by creating different thread for each peer which it serves.
     7) Update appropriately the data structures and the counters whenver is required after each notify(). For this purpose
     proper locking mechanisms and appropriate must be used data structures (eg ConcurrentHashMap) to avoid race conditions and deadlocks.
     8) Implements reply_list() function whenever a peer asks, using the list() function, for the available files which are available in the system.
     9) Implements the reply_details() function whenver gets asked by a peer, using details() function, for a file. Using the data structure from above | Tracker's 4th function | it finds the peer which have the file. Then confirms, for each peer, that it has not failed by sending the checkActive messages. If a peer has failed, updates the data structures appropriately and invalidates its token_id. Finally it responds with all running peers that have the file or a with a failure message in case the file does not exist in any peer in operation.

!!! IMPORTANT: All functions must print appropriate messages to the user.


Notes: You can assume that from the login time of a peer, its files on the file_directory does not change until it downloads a new file from other peers. Also, you can assume that to completely authenticate a file, you can do it by only using its name. So it is not possible to have 2 files with the same name.


7) Sockets:
     Trackers and peers will communicate with each other using sockets. A connection using a socket is essentialy a connection of two programs over the network. 
     A typical client-server flow with sockets is described as follows:
          - Server listening in a ServerSocket, which is associated with a specific port.
          - The clients uses a socket to connect to the port the server is listening to. Client must already know the hostname of the computer running the ServerSocket as well as the port number of the ServerSocket.
          - The server's ServerSocket accepts the client's connection, creates a new socket and listens about new clients.
          - The client and the server can now communicate by reading and writing through their sockets.
          - Finally they both close their sockets.
     In this particular application: 
          - The tracket will listen on a ServerSocket, which is associated with a specific one port.
          - Each peer also listens to a ServerSocket on which it waits either for download requests from other peers or checkActive message from tracker or peers. 
          - In other words, the will be two categories of connecitons depending on who initiates the connection and who it connects to. For the further functions register, login, addFile, search etc the connection is initiated by a peer and connects to the tracker's ServerSocket. For the operation of downloading a file the peer concerned initiates the connections and connects to the ServerSockets of the peers that have the file. Also the tracker and the peers can initiate a connection to a peer on its ServerSocket whenever the want to send checkActive messages.
          - The only port that should be considered known from the start is the one on which tracker listens to. All other can be chosen randomly.