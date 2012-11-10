"""
Base class for common operations of servers.
"""
import logging
import util


class BaseServer(object):

    def __init__(self):
        self.paths = {}
        util.register_all(self)

    def handler(self, method, uri, hdrs, res_start, req_pause):
        res_body, res_done = res_start(200, 'OK', {}, req_pause)

        self.paths.get(util.make_ident(method, uri), self.fourohfour)(res_body)
        res_done(None)

        # FIXME: The following are totally not the right thing to return
        return res_body, res_done

    def get_logger(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log

    def dispatch(self):
        return NotImplemented

    # HTTP verbs and paths below

    # FIXME: This sort of situation should return status code 404, not 200!
    def fourohfour(self, res_body):
        res_body('THAT DOESN\'T EXIST!')

    """
    Send the list of sites to access.
    """
    @util.register(method='GET', path='/hello')
    def gethello(self, res_body):
        res_body("HELLO THERE!")
