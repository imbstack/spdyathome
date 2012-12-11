#!/usr/bin/python
"""
9. same as plot1 except average across site
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    speed_diffs = {}
    for line in f:
        blob = json.loads(line)
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            if site in speed_diffs:
                speed_diffs[site].append(http - spdy)
            else:
                speed_diffs[site] = [http - spdy]
    avgs = [sum(x)/len(x) for x in speed_diffs.values()]
    for x in sorted(avgs):
        print x
