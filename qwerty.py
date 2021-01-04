import pickle
import socket

from pynput.keyboard import Controller

_keyboard = Controller()


def _live_stream(data, release_standard_value=200):
    key = pickle.loads(data)
    if len(data) > release_standard_value:
        _keyboard.release(key)
    else:
        _keyboard.press(key)


def main(host='', port=38042):
    with socket.create_server((host, port)) as server:
        print('qwerty is listening at port', port)
        conn, addr = server.accept()
        print('Standing by', addr)

        with conn:
            conn.send(b'Enemy Controller Activate!')
            while True:
                _live_stream(conn.recv(2048))


if __name__ == '__main__':
    main()
