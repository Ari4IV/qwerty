"""The qwerty module."""
import pickle
import socket
import time

from pynput.keyboard import Controller
from pynput.keyboard import Listener


class Qwerty:
    """The Qwerty object."""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_connection(self):
        """The create_connection() method."""
        with socket.create_connection((self.host, self.port)) as sock:
            sock.setblocking(False)

            try:
                print(f'qwerty: {sock.recv(26).decode()}')
            except BlockingIOError:
                pass

            def on_press(key):
                sock.sendall(pickle.dumps(key) + b'P')

            def on_release(key):
                sock.sendall(pickle.dumps(key) + b'R')

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

    def create_server(self):
        """The create_server() method."""
        with socket.create_server((self.host, self.port)) as server:
            print('qwerty is listening at port', self.port)

            server.setblocking(False)

            _keyboard = Controller()
            conns = []

            def _live_stream(data):
                key = pickle.loads(data)

                if data[-1] == 80:
                    _keyboard.press(key)
                else:
                    _keyboard.release(key)

            while True:
                try:
                    conn, addr = server.accept()
                except BlockingIOError:
                    pass
                else:
                    print('Standing by', addr)

                    conn.setblocking(False)
                    conn.send(b'Enemy Controller Activate!')

                    conns.append(conn)
                finally:
                    for conn in conns:
                        try:
                            _live_stream(conn.recv(1024))
                        except BlockingIOError:
                            pass

                    time.sleep(0.1)
