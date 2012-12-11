#!/usr/bin/python
"""
1. plot of difference between speeds
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    speed_diffs = []
    for line in f:
        blob = json.loads(line)
        count = 0
        good = 0
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            speed_diffs.append(http - spdy)
    for x in speed_diffs:
        print x
