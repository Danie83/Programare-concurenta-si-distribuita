import socket
import threading

# create a socket, get the local host, and connect
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
server_socket.bind((host, 65432))

# accepts a queue of n size, n is the max number of connections that can be queued
server_socket.listen(5)

# method for handling the client message
def handle_client(client_socket, address):
    while True:
        client_message = client_socket.recv(1024)

        if not client_message:
            break

        print("Received client message %s: %s" % (str(address), client_message.decode()))

        message = "Client messaged: %s!" % str(address)
        client_socket.send(message.encode())

    # closing the connection
    print("Closing connection: %s" % str(address))
    client_socket.close()

while True:
    # waiting for client to connect
    print("Waiting for connections...")
    client_socket, address = server_socket.accept()

    # handle clients on separate threads, each client is handled separately
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()
