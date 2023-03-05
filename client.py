import socket
import time
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

MESSAGE_SIZE_SELECTION = int(config_object["APPLICATIONSETUP"]["message_size_selection"])
MESSAGE_SIZES = config_object["APPLICATIONSETUP"]["message_sizes"].split(" ")
MESSAGE_SIZES = [int(x) for x in MESSAGE_SIZES]

CURRENT_MESSAGE_SIZE = MESSAGE_SIZES[MESSAGE_SIZE_SELECTION]

def tcp():
    # create a socket, get the local host, and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    client_socket.connect((host, 65432))

    with open("byte_file", "rb") as f:
        while True:
            # send chunk of data to the server
            data_chunk = f.read(CURRENT_MESSAGE_SIZE)
            if not data_chunk:
                break
            client_socket.send(data_chunk)

        # closing the connection
        client_socket.close()

if __name__ == '__main__':
    tcp()