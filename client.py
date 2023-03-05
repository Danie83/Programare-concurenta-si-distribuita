import socket

# create a socket, get the local host, and connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
client_socket.connect((host, 65432))

while True:
    # get user input, encode it (bytes) an send it to the server
    client_message = input("Enter a message to send to the server: ")
    client_socket.send(client_message.encode())

    # the server response to the message sent by the client
    server_response = client_socket.recv(1024)
    print("Server response: %s" % server_response.decode())

    # a way for the client to stop messaging (testing)
    continue_message = input("Do you want to send another message? (y/n) ")
    if continue_message.lower() != 'y':
        break

# closing the connection
client_socket.close()
