#!/usr/bin/python
"""
3. average over the course of a whole responder  otherwise same as plot1
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    speed_diffs = []
    for line in f:
        sd = []
        blob = json.loads(line)
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            sd.append(http - spdy)
        speed_diffs.append(sum(sd)/len(sd))
    for x in sorted(speed_diffs):
        print x
