"""
mitmproxy setup
"""

import os
from libmproxy import flow, proxy


class Instrument(flow.FlowMaster):
    def run(self):
        try:
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, r):
        f = flow.FlowMaster.handle_request(self, r)
        if f:
            r._ack()
        return f

    def handle_response(self, r):
        f = flow.FlowMaster.handle_response(self, r)
        if f:
            r._ack()
        print f
        return f


def setup_instrument(port):
    """
    Factory for the Instrument
    """
    config = proxy.ProxyConfig(
        cacert = os.path.expanduser("~/.mitmproxy/mitmproxy-ca.pem")
    )

    state = flow.State()
    server = proxy.ProxyServer(config, port)
    m = Instrument(server, state)
    m.run()
    return m
