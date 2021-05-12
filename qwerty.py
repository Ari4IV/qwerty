from pynput.keyboard import Controller

import socket, pickle

keyboard = Controller()

host = '0.0.0.0'
port = 38042
qwertyMessage = 'Enemy Controller Complete!'

with socket.create_server((host, port)) as server:
        print('qwerty is listening at port', port)
        connect, address = server.accept()
        print('Standing by', address)

        with connect:
            connect.send(qwertyMessage.encode())
            while True:
                qwerty = connect.recv(2048)
                key = pickle.loads(qwerty)
                if qwerty[-1] == 80:
                    keyboard.press(key)
                else:
                    keyboard.release(key)