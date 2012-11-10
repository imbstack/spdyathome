"""
Server to function as HTTP/1.1 endpoint for testing.
"""
from serverbase import BaseServer


class HTTPServer(BaseServer):

    def init(self):
        print "HTTP!"
