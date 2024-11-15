import socket
import threading
import sys

args = sys.argv

clients = {}  # Dictionary to store clients and their addresses


def handle_client(client_socket, client_address):
    """Handles communication with a connected client."""
    clients[client_address] = client_socket
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    try:
        while True:
            # Keep the connection alive
            pass
    except ConnectionResetError:
        print(f"[DISCONNECTION] {client_address} disconnected.")
    finally:
        del clients[client_address]
        client_socket.close()


def start_server(host='127.0.0.1', port=int(args[1])):
    """Starts the server and accepts connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[LISTENING] Server is listening on {host}:{port}")
    
    # Thread to accept clients
    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()

    while True:
        # Server-side prompt to send messages
        if clients:
            print("\n[CLIENTS] Active clients:")
            for i, addr in enumerate(clients.keys()):
                print(f"{i + 1}. {addr}")

            try:
                client_index = int(input("\nEnter the client number to send a message (0 to skip): ")) - 1
                if client_index < 0:
                    continue

                target_client = list(clients.values())[client_index]
                message = input("Enter the message to send: ")
                target_client.send(message.encode('utf-8'))
                print("[MESSAGE SENT]")
            except (ValueError, IndexError):
                print("[ERROR] Invalid client selection.")
    
def accept_clients(server):
    """Accepts new clients in a separate thread."""
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()

