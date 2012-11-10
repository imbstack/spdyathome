import argparse

from serverspdy import SPDYServer
from serverhttp import HTTPServer


def get_args():
    parser = argparse.ArgumentParser(
            description='Run SPDY and HTTP servers to act as endpoint of test.',
            epilog='This can be run directly or using `scripts/run-servers`.')
    parser.add_argument('-c', '-config', type=str, required=True,
            dest='conf_file', action='store', help='YAML configuration file.')
    return parser.parse_args()


def main():
    args = get_args()
    SPDYServer(args).start()
    HTTPServer(args).start()

if __name__ == '__main__':
    main()
