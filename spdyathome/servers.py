"""
Start the basic nbhttp servers for each case of connection.
Use the standard request responders in BaseServer.
"""
import yaml
import argparse
from nbhttp import run
from nbhttp.spdy_server import SpdyServer
from nbhttp.server import Server
from serverbase import BaseServer


def get_args():
    parser = argparse.ArgumentParser(
            description='Run SPDY and HTTP servers to act as endpoint of test.',
            epilog='This can be run directly or using `scripts/run-servers`.')
    parser.add_argument('-c', '-config', type=str, required=True,
            dest='conf_file', action='store', help='YAML configuration file.')
    return parser.parse_args()


def main():
    args = get_args()
    conf = yaml.load(file(args.conf_file, 'r'))
    print 'creating SPDY server on port %d' % (conf['spdy_port'],)
    spdy_base = BaseServer()
    SpdyServer(host='',
            port=conf['spdy_port'],
            request_handler=spdy_base.handler,
            log=spdy_base.get_logger('SPDY'))
    print 'creating HTTP server on port %d' % (conf['http_port'],)
    http_base = BaseServer()
    Server(host='',
            port=conf['http_port'],
            request_handler=http_base.handler,
            log=spdy_base.get_logger('HTTP'))
    run()
    # TODO: Kinda weird usage of (http|spdy)_base?  Think about changing that.

if __name__ == '__main__':
    main()
