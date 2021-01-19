"""Copyright 2021 BAIN5"""
import pickle
import socket
import sys

from pynput.keyboard import Controller
from pynput.keyboard import Listener


class Qwerty:
    """TODO(BAIN5)"""
    _keyboard = Controller()

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _live_stream(self, data):
        try:
            key = pickle.loads(data)
        except EOFError:
            print('Good Bye')
            sys.exit()
        if data[-1] == 80:
            Qwerty._keyboard.press(key)
        else:
            Qwerty._keyboard.release(key)

    def create_connection(self):
        """TODO(BAIN5)"""
        with socket.create_connection((self.host, self.port)) as sock:
            print(f'qwerty: {sock.recv(26).decode()}')

            def on_press(key):
                sock.send(pickle.dumps(key) + b'P')

            def on_release(key):
                sock.send(pickle.dumps(key) + b'R')

            with Listener(on_press=on_press, on_release=on_release) as listener:
                try:
                    listener.join()
                except KeyboardInterrupt:
                    print('Good Bye')
                    sys.exit()

    def create_server(self):
        """TODO(BAIN5)"""
        with socket.create_server((self.host, self.port)) as server:
            print('qwerty is listening at port', self.port)
            conn, addr = server.accept()
            print('Standing by', addr)

            with conn:
                conn.send(b'Enemy Controller Activate!')
                while True:
                    try:
                        self._live_stream(conn.recv(2048))
                    except pickle.UnpicklingError:
                        pass
