"""
Client testbed for running tests against the spdyathome server
"""

import sys
import httplib
from browse import browse
import proxy


def main():
    # TODO: set the port and such for the proxy in the config file
    pport = 8090
    #proxy.setup_instrument(pport)
    sitelist = [x.split()[0] for x in open(sys.argv[1], 'r')]
    for site in sitelist:
        # TODO: make the host settable in a config file
        print 'Connecting: localhost:8080/site/' + site
        # TODO: Turn this back into HTTPS
        h = httplib.HTTPConnection('localhost',  pport)
        h.set_tunnel('localhost', 8080)  # TODO: set this in the browser itself?
        b = browse(h)
        b.get(site)


if __name__ == '__main__':
    # TODO: Make this work with optparse or whatever
    if len(sys.argv) < 2:
        print 'Needs sitelist!'
        exit()
    main()
