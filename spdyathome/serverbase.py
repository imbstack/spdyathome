"""
Base class for common operations of servers.
"""
import logging


class BaseServer(object):

    def handler(self, method, uri, hdrs, res_start, req_pause):
        print method
        return '', 'YEP'

    def get_logger(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log
