#!/usr/bin/python
"""
10. scatter of speedup vs asset count
"""
import sys
import json

def load_list(f):
    ls = []
    for line in open(f, 'r'):
        ls.append(line.split()[0])
    return ls

if __name__ == '__main__':

    toplot = []

    sitelist = load_list(sys.argv[2])
    sites = {}
    for line in open(sys.argv[3], 'r'):
        j = json.loads(line)
        if str(j['id']) in sitelist:
            sites[str(j['id'])] = j

    f = open(sys.argv[1])

    for line in f:
        blob = json.loads(line)
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            # Print avg of time to download, difference in speed pairs
            print len(sites[site]['assets']), http - spdy
