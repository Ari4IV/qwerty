import pickle
import socket

from pynput.keyboard import Controller

from output import BANNER

_keyboard = Controller()


def _live_stream(data):
    key = pickle.loads(data)
    if data[-1] == 80:
        _keyboard.press(key)
    else:
        _keyboard.release(key)


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
    print(BANNER)
    main()
