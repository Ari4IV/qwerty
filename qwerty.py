from pynput.keyboard import Key, Controller

import socket, pickle

keyboard = Controller()

host = '0.0.0.0'
port = 38042


def _live_stream(data, release_standard_value=200):
    key = pickle.loads(data)
    if len(data) > release_standard_value:
        keyboard.release(key)
    else:
        keyboard.press(key)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    socket.bind((host, port))
    print("qwerty is listening at port", port)
    socket.listen()
    connect, address = socket.accept()
    qwertyMessage = 'Enemy Controller Activate!'
    connect.sendall(qwertyMessage.encode())
    with connect:
        print('Standing by', address)
        while True:
            _live_stream(connect.recv(2048))
