import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Client setup
HOST = '127.0.0.1'  # Server IP
PORT = 5000         # Server Port

def receive_messages():
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_area.config(state='normal')
                chat_area.insert('end', message + '\n')
                chat_area.yview('end')  # Auto-scroll to the latest message
                chat_area.config(state='disabled')
        except:
            print("Connection lost!")
            break

def send_message():
    """Sends a message to the server."""
    message = message_entry.get()
    if message and username:
        full_message = f"{username}: {message}"
        client_socket.send(full_message.encode('utf-8'))
        message_entry.delete(0, 'end')  # Clear the input field

def connect_to_server():
    """Connects to the server."""
    try:
        client_socket.connect((HOST, PORT))
        threading.Thread(target=receive_messages, daemon=True).start()
    except:
        print("Failed to connect to the server.")
        root.quit()

def set_username():
    """Sets the username and disables the username entry box."""
    global username
    username = username_entry.get().strip()
    if username:
        username_entry.config(state='disabled')
        username_button.config(state='disabled')
        connect_to_server()

# Create the GUI
root = tk.Tk()
root.title("Chat App")

# Username entry field
tk.Label(root, text="Enter Username:").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, width=20)
username_entry.grid(row=0, column=1, padx=10, pady=5)
username_button = tk.Button(root, text="Set Username", command=set_username)
username_button.grid(row=0, column=2, padx=10, pady=5)

# Chat area
chat_area = scrolledtext.ScrolledText(root, state='disabled', wrap='word', width=50, height=20)
chat_area.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Message entry field
message_entry = tk.Entry(root, width=40)
message_entry.grid(row=2, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = ""  # Global variable to store username

# Start the GUI loop
root.mainloop()

# Close the socket when the GUI is closed
client_socket.close()
