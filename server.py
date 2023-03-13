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

# streaming
def tcp_s():
    # create a socket using the config protocol, get the local host, and connect
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_socket.bind((host, 65432))

    # accepts a queue of n size, n is the max number of connections that can be queued
    server_socket.listen(5)

    client_socket, address = server_socket.accept()
    message_counter, bytes_read_counter = 0, 0
    start = time.time()
    while True:
        client_data = client_socket.recv(CURRENT_MESSAGE_SIZE)
        if not client_data or (len(client_data) == 4 and client_data.decode() == "stop"):
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

def udp_saw():
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
        server_socket.sendto("yes".encode(), address)

    print("Protocol used: UDP")
    print("Messages Counter: %d" % message_counter)
    print("Bytes Counter: %d" % bytes_read_counter) # includes "stop"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--protocol',
        default='tcp-s',
        choices=['tcp-s', 'udp-saw'],
        help="""
            Protocol type that is used to transmit data.
        """
    )
    args = parser.parse_args()
    config = vars(args)

    if config['protocol'] == 'udp_saw':
        udp_saw()
    else:
        tcp_s()
    