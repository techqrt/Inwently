import socket

from biller.config import Configurations

socket_clients = {}


class SocketApp:
    def __init__(self):
        self.host = Configurations.socket_server_connect['host']
        self.port = Configurations.socket_server_connect['port']

    def start_server(self):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        while True:
            try:
                # Accept incoming connection from a client
                client_socket, address = server_socket.accept()
                socket_clients[str(address)] = client_socket
                client_socket.sendall(str(address).encode())
                print(f"Accepted connection from {address[0]}:{address[1]}")

            except Exception as e:
                print(f"Error: {e}")
                break
        server_socket.close()
