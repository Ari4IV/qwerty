import pickle
import socket

from pynput.keyboard import Key
from pynput.keyboard import Listener

host = input('IP Address? :')
port = 38042

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))

qwertyMessage = str(socket.recv(2048), encoding='utf-8')
print('qwerty:', qwertyMessage)

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
    socket.send(pickle.dumps(key) * 1)

def on_release(key):
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
    socket.send(pickle.dumps(key) * 2)

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
