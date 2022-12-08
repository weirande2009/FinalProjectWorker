import socket
import numpy as np
from Worker import Worker


class Server:
    DATA_SIZE_LENGTH = 16

    def __init__(self, ip: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(True)
        # image recognition worker
        self.worker = Worker()

    def start(self):
        # wait for connection

        while True:
            try:
                client_sock, client_address = self.sock.accept()
                print(client_address)
                self.listen(client_sock)
            except:
                print("WebServer disconnects")
                continue

    def listen(self, client_sock):
        """
        Wait for connection from webserver and image
        :return:
        """
        # receive data
        height = int(self.receive_all(client_sock))
        width = int(self.receive_all(client_sock))
        data = self.receive_all(client_sock)
        # convert data to numpy
        image = np.frombuffer(data, dtype='uint8')
        image = image.reshape([height, width, 3])
        # recognize image
        name = self.worker.recognize(image)
        # send to client
        self.send(client_sock, name.encode())

    def receive_all(self, client, length=-1):
        """
        Receive all data from worker
        :param client: target client
        :param length: bytes number
        :return: the received data
        """
        if length == -1:
            length = int(self.receive_all(client, self.DATA_SIZE_LENGTH))
        buf = b''
        while length:
            new_buf = client.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
        return buf

    def send(self, client, data: bytes):
        client.send(str(len(data)).ljust(self.DATA_SIZE_LENGTH).encode())
        client.send(data)
