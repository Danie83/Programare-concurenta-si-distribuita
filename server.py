import socket
import threading
import time
from configparser import ConfigParser
import argparse

config_object = ConfigParser()
config_object.read("config.ini")

MESSAGE_SIZE_SELECTION = int(config_object["APPLICATIONSETUP"]["message_size_selection"])
MESSAGE_SIZES = config_object["APPLICATIONSETUP"]["message_sizes"].split(" ")
MESSAGE_SIZES = [int(x) for x in MESSAGE_SIZES]

CURRENT_MESSAGE_SIZE = MESSAGE_SIZES[MESSAGE_SIZE_SELECTION]

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
    print("Protocol used: TCP")
    print("Messages Counter: %d" % message_counter)
    print("Bytes Counter: %d" % bytes_read_counter)
    print("Total elapsed time: %d ms" % elapsed_time)

def udp():
    # create a socket using the config protocol, get the local host, and bind
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    server_socket.bind((host, 65430))

    message_counter, bytes_read_counter = 0, 0
    while True:
        data, address = server_socket.recvfrom(CURRENT_MESSAGE_SIZE)
        if not data or (len(data) == 4 and data.decode() == "stop"):
            break
        message_counter += 1
        bytes_read_counter += len(data)
        server_socket.sendto("test".encode(), address)

    print("Protocol used: UDP")
    print("Messages Counter: %d" % message_counter)
    print("Bytes Counter: %d" % bytes_read_counter) # includes "stop"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--protocol',
        default='tcp',
        choices=['tcp', 'udp'],
        help="""
            Protocol type that is used to transmit data.
        """
    )
    args = parser.parse_args()
    config = vars(args)

    if config['protocol'] == 'udp':
        udp()
    else:
        tcp()
    