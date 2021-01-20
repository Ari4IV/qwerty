"""The qwerty module."""
import pickle
import socket
import time

from pynput.keyboard import Controller
from pynput.keyboard import Listener

CPC = 0
CRC = 0
SPC = 0
SRC = 0


class Qwerty:
    """The Qwerty object."""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_connection(self):
        """The create_connection() method."""
        with socket.create_connection((self.host, self.port)) as sock:
            print(f'qwerty: {sock.recv(26).decode()}')

            def on_press(key):
                global CPC
                data = pickle.dumps(key) + b'P'
                sock.send(data)
                CPC += 1
                print(f'{CPC}\t[CP]: {len(data)}')

            def on_release(key):
                global CRC
                data = pickle.dumps(key) + b'R'
                sock.send(data)
                CRC += 1
                print(f'{CRC}\t[CR]: {len(data)}')

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

    def create_server(self):
        """The create_server() method."""
        _keyboard = Controller()

        def _live_stream(data):
            global SPC, SRC
            key = pickle.loads(data)
            if data[-1] == 80:
                _keyboard.press(key)
                SPC += 1
                print(f'{SPC}\t[SP]: {len(key)}')
            else:
                _keyboard.release(key)
                SRC += 1
                print(f'{SRC}\t[SR]: {len(key)}')

        with socket.create_server((self.host, self.port)) as server:
            print('qwerty is listening at port', self.port)
            conn, addr = server.accept()
            print('Standing by', addr)

            with conn:
                conn.send(b'Enemy Controller Activate!')
                while True:
                    try:
                        _live_stream(conn.recv(2048))
                    except pickle.UnpicklingError:
                        pass
