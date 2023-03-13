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

    with open("byte_file", "rb") as f:
        elapsed, message_counter, bytes_sent_counter = 0, 0, 0
        while True:
            # send chunk of data to the server
            start = time.time()
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.send(data_chunk)
            end = time.time()
            elapsed += end - start
            message_counter += 1
            bytes_sent_counter += len(data_chunk)

        # closing the connection
        client_socket.send("stop".encode())
        client_socket.close()
        print("Connection terminated.")
        print("Total transamission time: %d" % elapsed)
        print("Message counter: %d" % message_counter)
        print("Bytes counter: %d" % bytes_sent_counter)

#stop and wait
def udp_saw():
    # create a socket, get the local host, and bind
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    client_socket.bind((host, 65432))

    with open("byte_file", "rb") as f:
        elapsed, message_counter, bytes_sent_counter = 0, 0, 0
        while True:
            # send chunk of data to the server
            start = time.time()
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.sendto(data_chunk, (host, 65430))
            end = time.time()
            message_counter += 1
            bytes_sent_counter += len(data_chunk)
            elapsed += end - start
            ACK, _ = client_socket.recvfrom(CURRENT_MESSAGE_SIZE)
            if ACK.decode() == "yes":
                ACK = None
                continue
            while ACK is None:
                start = time.time()
                client_socket.sendto(data_chunk, (host, 65430))
                end = time.time()
                ACK, _ = client_socket.recvfrom(CURRENT_MESSAGE_SIZE)
                elapsed += end - start
        
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
        choices=['tcp-s', 'udp-saw'],
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