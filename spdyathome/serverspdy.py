"""
Server to function as SPDY endpoint for testing.
"""
from serverbase import BaseServer


class SPDYServer(BaseServer):

    def init(self):
        print "SPDY!"
