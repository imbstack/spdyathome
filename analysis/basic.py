#!/usr/bin/python
"""
Find which protocol was faster for each of the 2** sites.
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    for line in f:
        blob = json.loads(line)
        count = 0
        good = 0
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            count += 1
            if spdy < http:
                good += 1
        print '%f/%f' % (good, count)
