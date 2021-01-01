from pynput.keyboard import Key, Controller

import time
import socket, pickle

keyboard = Controller()

host = '0.0.0.0'
port = 38042

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
            data = connect.recv(2048)
            dedata = pickle.loads(data)
            keyboard.press(dedata)
            time.sleep(0.25)
            keyboard.release(dedata)