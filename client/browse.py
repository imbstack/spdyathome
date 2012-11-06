"""
Simulated browser that parses the page and collects the list
of assets that need to be fetched. It then fetches them.
"""


class browse:

    def __init__(self, conn):
        """
        Initialize with the required connection type.  This allows it to be used
        with either HTTP or SPDY and not need to know the difference.
        """
        self.conn = conn

    def get(self, site):
        self.conn.request('GET', '/site/'+ site)
        r = self.conn.getresponse()
        print r.status, r.reason
