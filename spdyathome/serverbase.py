"""
Base class for common operations of servers.
"""
import yaml


class BaseServer(object):

    def __init__(self, args):
        conf = yaml.load(file(args.conf_file, 'r'))
        print conf

    def start(self):
        print "Starting Server!"
        self.init()
