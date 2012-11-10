"""
Server to function as SPDY endpoint for testing.

Uses SpdyServer from nbhttp in order to handle the SPDY bits.
"""
from serverbase import BaseServer
from nbhttp import spdy_server, run


class SPDYServer(BaseServer):

    def init(self):
        print "starting SPDY server on port %d..." % (self.conf['spdy_port'],)
        spdy_server.SpdyServer('127.0.0.1',
                self.conf['spdy_port'],
                use_ssl=False,
                certfile=None,
                keyfile=None,
                request_handler=self.ret_list,
                log=self.get_logger('SPDY'))
        # TODO: This run() call is blocking. Make it so both servers can be
        # run simultaneously.
        run()
