"""
Copyright 2021 BAIN5

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import argparse
import pickle
import socket

from pynput.keyboard import Controller
from pynput.keyboard import Listener

from output import BANNER


class Qwerty:
    """TODO(BAIN5)"""
    _keyboard = Controller()

    def __init__(self, parser):
        self.host = parser.host
        self.port = parser.port
        self.mode = parser.mode

    def _live_stream(self, data):
        key = pickle.loads(data)
        if data[-1] == 80:
            Qwerty._keyboard.press(key)
        else:
            Qwerty._keyboard.release(key)

    def client(self, host, port):
        """TODO(BAIN5)"""
        with socket.create_connection((host, port)) as sock:
            print(f'qwerty: {sock.recv(26).decode()}')

            def on_press(key):
                sock.send(pickle.dumps(key) + b'P')

            def on_release(key):
                sock.send(pickle.dumps(key) + b'R')

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

    def server(self, host, port):
        """TODO(BAIN5)"""
        with socket.create_server((host, port)) as server:
            print('qwerty is listening at port', port)
            conn, addr = server.accept()
            print('Standing by', addr)

            with conn:
                conn.send(b'Enemy Controller Activate!')
                while True:
                    self._live_stream(conn.recv(2048))


def main():
    """TODO(BAIN5)"""
    parser = argparse.ArgumentParser()
    # Positional argument
    parser.add_argument(
        'host', help='specifies the hostname to contact over the network',
        metavar='hostname')

    # Optional arguments
    parser.add_argument('-l', action='store_false',
                        help='listen mode, for inbound connects', dest='mode')
    parser.add_argument('-p', default=38042, type=int,
                        help='specify alternate port [default: 38042]',
                        metavar='port', dest='port')

    qwerty = Qwerty(parser.parse_args())
    if not qwerty.mode:
        qwerty.server(qwerty.host, qwerty.port)
    else:
        qwerty.client(qwerty.host, qwerty.port)


if __name__ == '__main__':
    print(BANNER)
    main()
