"""
Start the basic nbhttp servers for each case of connection.
Use the standard request responders in BaseServer.
"""
import yaml
import argparse
from thor.loop import run
from nbhttp.spdy_server import SpdyServer
from nbhttp import push_tcp
from thor import HttpServer
from serverbase import BaseServer
from multiprocessing import Process


def get_args():
    parser = argparse.ArgumentParser(
            description='Run SPDY and HTTP servers to act as endpoint of test.',
            epilog='This can be run directly or using `scripts/run-servers`.')
    parser.add_argument('-c', '-config', type=str, required=True,
            dest='conf_file', action='store', help='YAML configuration file.')
    return parser.parse_args()


def http_main(cfile):
    conf = yaml.load(file(args.conf_file, 'r'))
    print 'Loading configuration into http base server!'
    base = BaseServer(conf)
    print 'creating HTTP server on port %d' % (conf['http_port'],)
    http_serve = HttpServer(host='', port=conf['http_port'])
    http_serve.on('exchange', base.http_handler)
    run()


def spdy_main(cfile):
    conf = yaml.load(file(args.conf_file, 'r'))
    print 'Loading configuration into spdy base server!'
    base = BaseServer(conf)
    print 'creating SPDY server on port %d' % (conf['spdy_port'],)
    SpdyServer('', conf['spdy_port'], base.spdy_handler)
    push_tcp.run()

if __name__ == '__main__':
    args = get_args()
    spdy = Process(target=spdy_main, args=(args.conf_file,))
    spdy.start()
    http = Process(target=http_main, args=(args.conf_file,))
    http.start()
    spdy.join()
    http.join()
