import socket, pickle

from pynput.keyboard import Key
from pynput.keyboard import Listener

host = input('IP Address? :')
port = 38042

with socket.create_connection((host, port)) as sock:
    print(f'qwerty: {sock.recv(2048).decode()}')

    def on_press(key):
        sock.send(pickle.dumps(key) + b'P')

    def on_release(key):
        sock.send(pickle.dumps(key) + b'R')

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()