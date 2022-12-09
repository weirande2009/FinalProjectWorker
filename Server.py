import socket
import numpy as np
from Worker import Worker
import struct


class Server:
    DATA_SIZE_LENGTH = 16

    def __init__(self, ip: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            except KeyboardInterrupt:
                exit(-1)
            except Exception as e:
                print(e)
                print("WebServer disconnects")
                continue

    def listen(self, client_sock):
        """
        Wait for connection from webserver and image
        :return:
        """
        while True:
            # receive data
            # height_data = self.receive_all(client_sock)
            # width_data = self.receive_all(client_sock)
            # print("height:", height_data)
            # print("width:", width_data)
            # height = int(height_data)
            # width = int(width_data)
            data = self.receive_all(client_sock)
            # convert data to numpy
            image = np.frombuffer(data, dtype='uint8')
            image = image.reshape([224, 224, 3])
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
            buf = b''
            l = struct.calcsize('!i')
            while l > 0:
                buf += client.recv(l)
                l -= len(buf)
            length = struct.unpack('!i', buf[:4])[0]
        buf = b''
        received_length = 0
        print("Expected length:", length)
        while length:
            new_buf = client.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
            received_length += len(new_buf)
        print("Received length:", received_length)
        return buf

    def send(self, client, data: bytes):
        val = struct.pack('!i', len(data))
        print(val)
        client.sendall(val)
        print(data)
        client.sendall(data)
