# Secure Chat Application with SSL Encryption

A secure real-time chat application built with Python. The application uses a client-server architecture, SSL/TLS encryption, multithreading, a Tkinter graphical user interface, and automatic conversation logging.

## Features

* Real-time messaging between multiple clients
* SSL/TLS encrypted communication
* Multi-client support using Python threading
* Tkinter graphical user interface
* Username-based messaging
* Automatic conversation logging
* Timestamped messages
* Client connection and disconnection tracking
* Self-signed SSL certificate support

## Technologies Used

* Python 3
* `socket`
* `ssl`
* `threading`
* `tkinter`
* `datetime`
* `cryptography`

## Project Structure

```text
secure-chat-app/
│
├── server/
│   ├── server.py
│   └── chat_log.txt
│
├── client/
│   ├── client.py
│   └── gui_client.py
│
├── certificates/
│   ├── cert.pem
│   └── key.pem
│
└── generate_cert.py
```

## How It Works

The application uses a central server to manage client connections and message broadcasting.

1. The server starts and loads the SSL certificate and private key.
2. Clients connect to the server through an SSL/TLS secured socket.
3. Each connected client is handled using a separate thread.
4. When a user sends a message, the server receives it and adds a timestamp.
5. The message is saved to `chat_log.txt`.
6. The server broadcasts the message to the other connected clients.
7. Messages are displayed in real time through the client interface.

## Installation

Make sure Python 3 is installed.

Install the required external package:

```bash
pip install cryptography
```

The remaining modules are included with Python.

## Generate SSL Certificate

If the certificate files are not already available, run:

```bash
python generate_cert.py
```

This will generate:

```text
certificates/cert.pem
certificates/key.pem
```

The certificate is self-signed and intended for educational and local development purposes.

## Run the Server

From the main project folder, run:

```bash
python server/server.py
```

The server should display:

```text
Secure chat server started on 127.0.0.1:5000
```

## Run the GUI Client

Open another terminal and run:

```bash
python client/gui_client.py
```

Open a second client window to test communication between multiple users:

```bash
python client/gui_client.py
```

Enter a username, click **Connect**, and begin sending messages.

## Console Client

A console-based client is also included and can be started with:

```bash
python client/client.py
```

## Conversation Logging

All messages are automatically stored in:

```text
server/chat_log.txt
```

Each message contains a timestamp and the sender's username.

Example:

```text
[2026-08-18 11:30:15] User1: Hello
[2026-08-18 11:30:20] User2: Hi
```

## Security

The application uses Python's `ssl` module to encrypt communication between the client and server.

A self-signed SSL certificate is used for this project. Client certificate verification is disabled for local development, so the connection is encrypted but the server identity is not verified by a trusted Certificate Authority.

For a production environment, a trusted SSL/TLS certificate and certificate verification should be used.

## Limitations

* Designed mainly for local network use
* Uses a self-signed SSL certificate
* No user authentication system
* No private messaging
* No file transfer
* Chat history is stored in a text file instead of a database

## Future Improvements

Possible improvements include:

* User login and authentication
* SQLite or MySQL database integration
* Private messaging
* Group chat support
* File transfer
* End-to-end encryption
* Server administration GUI
* Online deployment

## Purpose

This project was developed as an educational networking and security project to demonstrate practical concepts including Python socket programming, SSL/TLS encryption, multithreading, graphical user interface development, and secure real-time communication.
