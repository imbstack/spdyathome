"""
Base class for common operations of servers.
"""
import util
import copy
import json
from thor.events import on
from nbhttp.http_common import dummy


class BaseServer(object):

    def __init__(self, conf):
        self.paths = {}
        util.register_all(self)
        self.sitelist = util.load_list(conf['sitelist'])
        self.sites = {}
        for i,line in enumerate(open(conf['sitedump'], 'r')):
            if str(i) in self.sitelist:
                self.sites[str(i)] = json.loads(line)

    def spdy_handler(self, method, uri, hdrs, res_start, req_pause):
        code = "200"
        phrase = "OK"
        res_hdrs = [('Content-Type', 'text/plain'), ('version', 'HTTP/1.1')]
        res_body, res_done = res_start(code, phrase, res_hdrs, dummy)
        res_body('This is SPDY.')
        res_done(None)
        return dummy, dummy

    def http_handler(self, x):
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

    # HTTP verbs and paths below

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
        try:
            site = copy.deepcopy(self.sites[str(index)])
        except KeyError:
            self.fourohfour(res)
            return
        if int(site['assets']['asset0']['size']) == 0:
            reqsize = int(site['assets'].pop('asset1'))
            site['assets'].pop('asset0')
        else:
            reqsize = int(site['assets'].pop('asset0')['size'])
        data['list'] = util.make_assets(site)
        print reqsize
        print len(str(data))
        data['junk'] = util.fill_junk(reqsize - len(str(data)))
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
        junk = util.fill_junk(int(size))
        res.response_start(200, 'OK', headers)
        res.response_body(junk)
        res.response_done([])
