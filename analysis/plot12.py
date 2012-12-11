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
        sd = []
        avgs = []
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            sd.append(http - spdy)
            avgs.append((http + spdy)/2)
        # Print avg of time to download, difference in speed pairs
        print sum(avgs)/len(avgs), sum(sd)/len(sd)
