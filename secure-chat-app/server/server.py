import socket
import ssl
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

clients = []


def log_message(message):
    """Save messages and system events to the chat log file."""
    with open("server/chat_log.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")


def broadcast(message, sender_socket):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                if client in clients:
                    clients.remove(client)


def handle_client(client_socket, address):
    """Receive messages from one client and broadcast them."""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if not message:
                break

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"[{timestamp}] {message}"

            print(full_message)
            log_message(full_message)
            broadcast(full_message, client_socket)

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)

    disconnect_message = f"[SYSTEM] Client disconnected: {address}"
    print(disconnect_message)
    log_message(disconnect_message)

    client_socket.close()


def start_server():
    """Start the secure SSL chat server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="certificates/cert.pem",
        keyfile="certificates/key.pem"
    )

    secure_server = context.wrap_socket(server_socket, server_side=True)

    print(f"Secure chat server started on {HOST}:{PORT}")
    log_message(f"[SYSTEM] Secure chat server started on {HOST}:{PORT}")

    while True:
        client_socket, address = secure_server.accept()

        connect_message = f"[SYSTEM] Client connected: {address}"
        print(connect_message)
        log_message(connect_message)

        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )
        thread.start()


start_server()