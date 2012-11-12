"""
Base class for common operations of servers.
"""
import logging
import util
import json
from thor.events import on


class BaseServer(object):

    def __init__(self, conf):
        self.paths = {}
        util.register_all(self)
        self.sites = json.loads(open(conf['sitedump'], 'r').read())
        self.sitelist = util.load_list(conf['sitelist'])

    def handler(self, x):
        @on(x, 'request_start')
        def go(*args):
            print "start: %s on %s" % (str(args[1]), id(x.http_conn))
            self.paths.get(util.make_ident(x.method, x.uri), self.fourohfour)(x)

        @on(x, 'request_body')
        def body(chunk):
            print "body: %s" % chunk

        @on(x, 'request_done')
        def done(trailers):
            print "done: %s" % str(trailers)

    def get_logger(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log

    # HTTP verbs and paths below

    # FIXME: This sort of situation should return status code 404, not 200!
    def fourohfour(self, res):
        headers = []
        res.response_start(404, 'Error Not Found', headers)
        res.response_body('THAT DOESN\'T EXIST!')
        res.response_done([])

    """
    Send the list of sites to access.
    """
    @util.register(method='GET', path='/hello')
    def gethello(self, res):
        headers = []
        res.response_start(200, 'OK', headers)
        # TODO: Generate this list from a file of top 100, etc.
        res.response_body(json.dumps(self.sitelist))
        res.response_done([])

    """
    For a given site, return the assets to acquire.
    """
    @util.register(method='GET', path='/site/')
    def getsite(self, res):
        headers = []
        index = int(res.uri.split('/')[-1])
        data = {'index': index}
        data['list'] = util.make_assets(self.sites[str(index)])
        # TODO: pass in size of original asset to fill_junk (also take into
        # account asset type for compression reasons!?
        data['junk'] = util.fill_junk(1)
        res.response_start(200, 'OK', headers)
        res.response_body(json.dumps(data))
        res.response_done([])

    """
    For a given asset, return a blob that is the size of the asset.
    Take into account compressibility.
    """
    @util.register(method='GET', path='/asset/')
    def getasset(self, res):
        headers = []
        asset = res.uri.split('/')[-1]
        size, comp = asset.split('.')
        size = int(size)
        # FIXME: This is not necessarily what the compression factor should be
        if comp == 'c':
            size *= 0.7
        junk = util.fill_junk(size)
        res.response_start(200, 'OK', headers)
        res.response_body(junk)
        res.response_done([])
