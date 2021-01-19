"""The parser module."""
import argparse


def parse_args():
    """The parse_args() function."""
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument(
        '-l', action='store_true', help='listen mode, for inbound connects',
        dest='listen_mode')
    parser.add_argument(
        '-p', default=38042, type=int,
        help='specify alternate port [default: 38042]', metavar='port',
        dest='port')

    # Positional argument
    parser.add_argument(
        'host', help='specifies the hostname to contact over the network',
        metavar='hostname')

    return parser.parse_args()
