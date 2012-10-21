import cherrypy
import sys
import random
import string
import json
import copy

sitemap = {}


class FauxPage(object):

    @cherrypy.expose
    def index(self):
        return "Welcome to spdy@home!"

    @cherrypy.expose
    def site(self, _id):
        site = copy.deepcopy(sitemap[int(_id)])
        # If there is an asset0 with a length of 0, we experienced a redirect
        # and should skip it in considering size.
        if int(site['asset0']) == 0:
            reqsize = int(site.pop('asset1'))
            site.pop('asset0')
        else:
            reqsize = int(site.pop('asset0'))
        out = '<html><head></head><body>' + ''.join(['<img src="/img/%s">'%(size,) for _,size in site.items()])
        diff = reqsize - len(out)
        out += '<script>' + ''.join([random.choice(string.letters) for i in xrange(diff)]) + '</script></body></html>'
        return out

    @cherrypy.expose
    def img(self, size):
        #TODO: Make this function aware of asset type and consider compression!
        chars = ''.join([random.choice(string.letters) for i in xrange(int(size))])
        return chars


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Need to specify data file!\nExample: python server.py <datafile>"
        exit()
    for line in open(sys.argv[1], 'r').readlines():
        l = json.loads(line)
        sitemap[l.pop('id')] = l
    cherrypy.quickstart(FauxPage())
