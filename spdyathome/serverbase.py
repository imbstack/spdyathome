"""
Base class for common operations of servers.
"""
import logging
import util
import json


class BaseServer(object):

    def __init__(self):
        self.paths = {}
        util.register_all(self)

    def handler(self, method, uri, hdrs, res_start, req_pause):

        self.paths.get(util.make_ident(method, uri), self.fourohfour)(res_start)

        # FIXME: The following are totally not the right thing to return
        return lambda x: x, lambda y: y

    def get_logger(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log

    # HTTP verbs and paths below

    # FIXME: This sort of situation should return status code 404, not 200!
    def fourohfour(self, res_start):
        headers = []
        res_body, res_done = res_start(404, 'Error Not Found', headers, None)
        res_body('THAT DOESN\'T EXIST!')
        res_done(None)

    """
    Send the list of sites to access.
    """
    @util.register(method='GET', path='/hello')
    def gethello(self, res_start):
        headers = []
        # FIXME: This should not have none for pause
        res_body, res_done = res_start(200, 'OK', headers, None)
        # TODO: Generate this list from a file of top 100, etc.
        res_body(json.dumps([1,77,23,11]))
        res_done(None)
