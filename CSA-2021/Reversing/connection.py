import socket
import time


class Socket:
    def __init__(self, host, port):
        self.conn = None
        self.host = host
        self.port = port
        self.is_connected = False

    def connect(self, print_first_msg=False):
        self.conn = socket.socket()
        self.conn.connect((self.host, self.port))
        self.is_connected = True
        msg = self.recv()
        if print_first_msg:
            print(msg.decode())
        return msg

    def recv(self, buffer_size=4096):
        msg = self.conn.recv(buffer_size)
        return msg

    def send(self, decoded_msg=""):
        self.conn.send((decoded_msg + "\n").encode())
        time.sleep(0.1)
        return self.recv()

    def close(self):
        self.conn.close()
        self.is_connected = False
