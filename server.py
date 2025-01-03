import socket
import threading

# Server setup
HOST = '127.0.0.1'  # Localhost (can replace with your IP for LAN)
PORT = 5000         # Port number

# List to keep track of connected clients
clients = []

# Function to handle communication with a client
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break
    
    # Remove disconnected client
    print("Client disconnected")
    clients.remove(client_socket)
    client_socket.close()

# Function to broadcast message to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Don't send the message to the sender
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on {HOST}:{PORT}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection: {client_address}")
        clients.append(client_socket)
        
        # Start a new thread for the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
