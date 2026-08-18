import socket
import ssl
import threading

HOST = "127.0.0.1"
PORT = 5000

username = input("Enter your name: ")

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if message:
                print("\n" + message)
            else:
                break

        except:
            print("Disconnected from server.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    secure_client = context.wrap_socket(client_socket, server_hostname=HOST)
    secure_client.connect((HOST, PORT))

    print("Connected to secure chat server.")
    print("Type your message below. Type 'exit' to quit.")

    thread = threading.Thread(target=receive_messages, args=(secure_client,))
    thread.daemon = True
    thread.start()

    while True:
        message = input()

        if message.lower() == "exit":
            break

        full_message = f"{username}: {message}"
        secure_client.send(full_message.encode("utf-8"))

    secure_client.close()

start_client()