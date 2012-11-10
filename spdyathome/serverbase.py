"""
Base class for common operations of servers.
"""
import logging


class BaseServer(object):

    def handler(self, method, uri, hdrs, res_start, req_pause):
        res_body, res_done = res_start(200, 'OK', {}, req_pause)

        res_body("THIS IS THE WINNER!")
        res_done(None)

        # FIXME: The following are totally not the right thing to return
        return res_body, res_done

    def get_logger(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log
