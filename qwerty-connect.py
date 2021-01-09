import pickle
import socket

from pynput.keyboard import Key
from pynput.keyboard import Listener


def main(host, port=38042):
    with socket.create_connection((host, port)) as sock:
        print(f'qwerty: {sock.recv(26).decode()}')

        def on_press(key):
            sock.send(pickle.dumps(key) + b'P')

        def on_release(key):
            sock.send(pickle.dumps(key) + b'R')

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


if __name__ == '__main__':
    host = input('IP Address? :')
    main(host)
