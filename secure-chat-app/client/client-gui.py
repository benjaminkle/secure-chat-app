import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = "127.0.0.1"
PORT = 5000


class SecureChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure SSL Chat Client")
        self.root.geometry("500x500")

        self.client_socket = None
        self.secure_client = None
        self.username = ""

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self.root, width=40)
        self.username_entry.pack(pady=5)

        self.connect_button = tk.Button(
            self.root,
            text="Connect",
            command=self.connect_to_server
        )
        self.connect_button.pack(pady=5)

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=55,
            height=20,
            state="disabled"
        )
        self.chat_area.pack(pady=10)

        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(
            self.root,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(pady=5)

    def connect_to_server(self):
        self.username = self.username_entry.get().strip()

        if not self.username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            self.secure_client = context.wrap_socket(
                self.client_socket,
                server_hostname=HOST
            )

            self.secure_client.connect((HOST, PORT))

            self.display_message("Connected to secure chat server.")
            self.connect_button.config(state="disabled")
            self.username_entry.config(state="disabled")

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

        except Exception as error:
            messagebox.showerror("Connection Error", str(error))

    def receive_messages(self):
        while True:
            try:
                message = self.secure_client.recv(1024).decode("utf-8")

                if message:
                    self.display_message(message)
                else:
                    break

            except:
                self.display_message("Disconnected from server.")
                break

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            return

        if self.secure_client is None:
            messagebox.showerror("Error", "Please connect to the server first.")
            return

        try:
            full_message = f"{self.username}: {message}"
            self.secure_client.send(full_message.encode("utf-8"))

            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

        except Exception as error:
            messagebox.showerror("Send Error", str(error))

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def close_connection(self):
        try:
            if self.secure_client:
                self.secure_client.close()
        except:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.close_connection)
    root.mainloop()