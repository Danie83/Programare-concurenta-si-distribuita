import socket
import time
from configparser import ConfigParser
import argparse

config_object = ConfigParser()
config_object.read("config.ini")

MESSAGE_SIZE_SELECTION = int(config_object["APPLICATIONSETUP"]["message_size_selection"])
MESSAGE_SIZES = config_object["APPLICATIONSETUP"]["message_sizes"].split(" ")
MESSAGE_SIZES = [int(x) for x in MESSAGE_SIZES]

CURRENT_MESSAGE_SIZE = MESSAGE_SIZES[MESSAGE_SIZE_SELECTION]

#streaming
def tcp_s():
    # create a socket, get the local host, and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    client_socket.connect((host, 65432))

    start = time.time()
    elapsed = 0
    with open("byte_file", "rb") as f:
        message_counter, bytes_sent_counter = 0, 0
        while True:
            # send chunk of data to the server
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.send(data_chunk)
            message_counter += 1
            bytes_sent_counter += len(data_chunk)

    end = time.time()
    elapsed = end - start
    # closing the connection
    client_socket.send("stop".encode())
    client_socket.close()
    print("Connection terminated.")
    print("Total transamission time: %d" % elapsed)
    print("Message counter: %d" % message_counter)
    print("Bytes counter: %d" % bytes_sent_counter)

def tcp_saw():
    # create a socket, get the local host, and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    client_socket.connect((host, 65432))

    start = time.time()
    elapsed = 0
    ACK = None
    with open("byte_file", "rb") as f:
        message_counter, bytes_sent_counter = 0, 0
        while True:
            # send chunk of data to the server
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.send(data_chunk)
            message_counter += 1
            bytes_sent_counter += len(data_chunk)
            ACK = client_socket.recv(CURRENT_MESSAGE_SIZE)
            if ACK.decode() == "yes":
                ACK = None
                continue
            while ACK is None:
                client_socket.send(data_chunk)
                ACK = client_socket.recv(CURRENT_MESSAGE_SIZE)

    end = time.time()
    elapsed = end - start
    # closing the connection
    client_socket.send("stop".encode())
    client_socket.close()
    print("Connection terminated.")
    print("Total transamission time: %d" % elapsed)
    print("Message counter: %d" % message_counter)
    print("Bytes counter: %d" % bytes_sent_counter)

#stop and wait
def udp_saw():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    client_socket.bind((host, 65432))

    start = time.time()
    elapsed = 0
    ACK = None
    with open("byte_file", "rb") as f:
        message_counter, bytes_sent_counter = 0, 0
        while True:
            # send chunk of data to the server
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.sendto(data_chunk, (host, 65430))
            message_counter += 1
            bytes_sent_counter += len(data_chunk)
            elapsed += end - start
            ACK, _ = client_socket.recvfrom(CURRENT_MESSAGE_SIZE)
            if ACK.decode() == "yes":
                ACK = None
                continue
            while ACK is None:
                client_socket.sendto(data_chunk, (host, 65430))
                ACK, _ = client_socket.recvfrom(CURRENT_MESSAGE_SIZE)
    end = time.time()
    elapsed = end - start
        
    print("Finished sening data.")
    print("Transmission time: %d" % elapsed)
    print("Messages count: %d" % message_counter)
    print("Bytes sent: %d" % bytes_sent_counter)
    client_socket.sendto("stop".encode(), (host, 65430))
    client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--protocol',
        default='tcp-s',
        choices=['tcp-s', 'udp-saw', 'tcp-saw'],
        help="""
            Protocol type that is used to transmit data.
        """
    )
    args = parser.parse_args()
    config = vars(args)

    if config['protocol'] == 'udp-saw':
        udp_saw()
    else:
        tcp_s()