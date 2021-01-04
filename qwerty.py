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


def main():
    with socket.create_server((host, port)) as server:
        print('qwerty is listening at port', port)
        conn, addr = server.accept()
        print('Standing by', addr)

        with conn as c:
            c.send(b'Enemy Controller Activate!')
            while True:
                _live_stream(c.recv(2048))


if __name__ == '__main__':
    main()
