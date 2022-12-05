import socket
import torch
import time
from Worker import Worker
# model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)


class Server:
    DATA_SIZE_LENGTH = 16

    def __init__(self, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", port))
        self.sock.listen(True)
        # wait for connection
        client_sock, client_address = self.sock.accept()
        # image recognition worker
        self.worker = Worker()

    def working(self):
        pass

    def receive_all(self, length):
        """
        Receive all data from worker
        :param length: bytes number
        :return: the received data
        """
        if length == -1:
            length = int(self.receive_all(self.DATA_SIZE_LENGTH))
        buf = b''
        while length:
            new_buf = self.sock.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
        return buf

class ProcessorPool:

    def __init__(self, num):
        self.workerNum = num  # have num workers in total
        self.workerList = [Worker() for i in range(num)]
        self.temporaryStore = ""

    def callAWorker(self, str_data):
        self.temporaryStore = str_data

        while True:
            for worker in self.workerList:
                if not worker.isOccupied:  # if this worker is not occupied
                    return worker.recognize(str_data)  # return result from the worker

            # all workers are currently occupied
            # wait for 3 sec before calling a worker again
            print("all workers are currently occupied...")
            time.sleep(3.0)


# def main():
#     ip = 'localhost'
#     port = 6002
#
#     # 初始化socket，设置为监听状态
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((ip, port))
#     s.listen(True)
#
#     # 等待并接收数据
#     conn, address = s.accept()
#     length = receive_all(conn, 16)
#     str_data = receive_all(conn, int(length))
#     s.close()
#
#     # 接收二进制数据流解码
#     data = np.fromstring(str_data, dtype='uint8')
#     decode_img = cv2.imdecode(data, 1)
#     cv2.imshow('serve', decode_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
