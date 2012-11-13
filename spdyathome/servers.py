"""
Start the basic nbhttp servers for each case of connection.
Use the standard request responders in BaseServer.
"""
import yaml
import logging
import argparse
from thor.loop import run
from nbhttp.spdy_server import SpdyServer
from nbhttp import push_tcp
from thor import HttpServer
from serverbase import BaseServer
from multiprocessing import Process
from thor.events import on
import urilib
import util


def get_args():
    parser = argparse.ArgumentParser(
            description='Run SPDY and HTTP servers to act as endpoint of test.',
            epilog='This can be run directly or using `scripts/run-servers`.')
    parser.add_argument('-c', '-config', type=str, required=True,
            dest='conf_file', action='store', help='YAML configuration file.')
    return parser.parse_args()


def http_main(cfile):
    conf = yaml.load(file(cfile, 'r'))
    print 'Loading configuration into http base server!'
    base = BaseServer(conf)
    print 'creating HTTP server on port %d' % (conf['http_port'],)

    def http_handler(x):
        @on(x, 'request_start')
        def go(*args):
            print "HTTP: start %s" % (str(args[1]),)
            base.paths.get(util.make_ident(x.method, x.uri), base.fourohfour)(x)

        @on(x, 'request_body')
        def body(chunk):
            print "body: %s" % chunk

        @on(x, 'request_done')
        def done(trailers):
            print "done: %s" % str(trailers)

    http_serve = HttpServer(host='', port=conf['http_port'])
    http_serve.on('exchange', http_handler)
    run()


def spdy_main(cfile):
    conf = yaml.load(file(cfile, 'r'))
    log = logging.getLogger('SPDY')
    print 'Loading configuration into spdy base server!'
    base = BaseServer(conf)
    print 'creating SPDY server on port %d' % (conf['spdy_port'],)

    def spdy_handler(method, uri, hdrs, res_start, req_pause):
        path = urilib.URI(uri).path
        print "SPDY: start %s" % (path,)
        met = base.paths.get(util.make_ident(method, path), base.fourohfour)
        met(util.resmap(res_start, uri))

        def body(chunk):
            print "body: %s" % chunk

        def done(trailers):
            print "done: %s" % str(trailers)

        return  body, done

    SpdyServer('0.0.0.0', conf['spdy_port'], spdy_handler, log)
    push_tcp.run()

if __name__ == '__main__':
    args = get_args()
    spdy = Process(target=spdy_main, args=(args.conf_file,))
    spdy.start()
    http = Process(target=http_main, args=(args.conf_file,))
    http.start()
    spdy.join()
    http.join()
