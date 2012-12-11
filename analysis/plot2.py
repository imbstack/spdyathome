#!/usr/bin/python
"""
2. scatter of speed difference vs total time taken
"""
import sys
import json

if __name__ == '__main__':
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
            print (http + spdy)/2, http - spdy
