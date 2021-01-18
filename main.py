"""The main module."""
from parser import parse_args
from qwerty import Qwerty
import output


def main():
    """The main() function."""
    print(output.BANNER)

    namespace = parse_args()
    qwerty = Qwerty(namespace.host, namespace.port)

    if namespace.listen_mode:
        qwerty.create_server()

    qwerty.create_connection()


if __name__ == '__main__':
    main()
