import socket
import threading
import time
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

MESSAGE_SIZE_SELECTION = int(config_object["APPLICATIONSETUP"]["message_size_selection"])
MESSAGE_SIZES = config_object["APPLICATIONSETUP"]["message_sizes"].split(" ")
MESSAGE_SIZES = [int(x) for x in MESSAGE_SIZES]

CURRENT_MESSAGE_SIZE = MESSAGE_SIZES[MESSAGE_SIZE_SELECTION]
PROTOCOL_TYPE = config_object["APPLICATIONSETUP"]["protocol_type"]

def tcp():
    # create a socket using the config protocol, get the local host, and connect
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_socket.bind((host, 65432))

    # accepts a queue of n size, n is the max number of connections that can be queued
    server_socket.listen(5)

    while True:
        # waiting for client to connect
        print("Waiting for connections...")
        client_socket, address = server_socket.accept()

        # handle clients on separate threads, each client is handled separately
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

# method for handling the client message
def handle_client(client_socket, address):
    message_counter, bytes_read_counter = 0, 0
    start = time.time()
    while True:
        client_data = client_socket.recv(CURRENT_MESSAGE_SIZE)

        if not client_data:
            break
        message_counter += 1
        bytes_read_counter += len(client_data)

    # closing the connection
    print("Closing connection: %s" % str(address))
    client_socket.close()
    end = time.time()
    elapsed_time = end - start
    print("Protocol used: %s" % PROTOCOL_TYPE)
    print("Messages Counter: %d" % message_counter)
    print("Bytes Counter: %d" % bytes_read_counter)
    print("Total elapsed time: %d ms" % elapsed_time)


if __name__ == '__main__':
    tcp()