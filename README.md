# P2P File System in Python

## Overview

This project implements a Peer-to-Peer (P2P) File System in Python, comprising a system with one tracker and multiple similar peers. Each peer maintains a shared directory containing files available for sharing within the network. Peers connect to the tracker to exchange information about available files and facilitate file transfers among themselves. The system is designed to support simultaneous connections and robust file sharing functionalities.

## System Components

### Tracker

- The tracker manages peer accounts and facilitates file sharing among peers.
- It maintains data structures for storing peer information, such as usernames, passwords, download counts, and failure counts.
- Supported functions include registration, login, and logout.
- The tracker utilizes multiple threads to handle simultaneous connections from peers efficiently.
- Functions such as `reply_list()` and `reply_details()` provide information about available files and their details, respectively.
- Sockets are used for communication between the tracker and peers, enabling reliable data exchange over the network.

### Peer

- Each peer interacts with the tracker and other peers using sockets.
- Peers maintain a shared directory containing files available for sharing.
- Key functionalities include file sharing, account management, and file retrieval.
- Peers register, login, and logout with the tracker to participate in the P2P network.
- The `simpleDownload()` function selects the best peer for file download based on responsiveness and reliability metrics.
- Sockets enable peer-to-peer communication for file transfers and status checks.

## Peer Functions

1. **Communicate with Tracker and Peers**: Peers establish connections with the tracker and other peers using sockets.
2. **Shared Directory**: Each peer maintains a shared directory containing files available for sharing.
3. **Account Management**: Peers register, login, and logout with the tracker to participate in the P2P network.
4. **File Sharing**: Peers inform the tracker about available files in their shared directory and request information about files of interest.
5. **List Available Files**: Peers retrieve a list of available files from the tracker.
6. **File Details**: Peers request details about a specific available file from the tracker.
7. **Check Peer Activity**: Peers verify the activity status of other peers in the network.
8. **Download Files**: Peers initiate file downloads from other peers based on availability and reliability metrics.

## Tracker Functions

1. **Manage Peer Accounts**: The tracker maintains peer account information and handles registration, login, and logout requests.
2. **Data Structures**: Appropriate data structures store peer information, file availability, and download statistics.
3. **Handle Peer Requests**: The tracker responds to peer requests for file lists and file details, ensuring data consistency and accuracy.
4. **Support Multiple Connections**: The tracker supports simultaneous connections from multiple peers by creating separate threads.
5. **Socket Communication**: Sockets facilitate communication between the tracker and peers, enabling real-time data exchange.

## Socket Communication

- Sockets are utilized for communication between the tracker and peers.
- The tracker listens on a specific port for incoming connections from peers.
- Peers also listen on ports for incoming requests and connections from other peers.
- Connections are initiated based on the type of operation, such as registration, login, file download, or status checks.
- The port used by the tracker is predetermined, while peers may choose random ports for communication.

---

By implementing this P2P File System in Python, users can efficiently share files among peers while ensuring reliability and data integrity. The system's design enables seamless communication and robust file transfer functionalities, making it suitable for various collaborative and distributed applications.
