#!/usr/bin/python
"""
5. whisker plot for any multiple responders
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    sites = {}
    for line in f:
        blob = json.loads(line)
        for site,vals in blob.items():
            if type(vals) != dict:
                continue
            spdy = float(vals['spdy']['time'])
            http = float(vals['http']['time'])
            if spdy == -1 or http == -1:
                continue
            if site in sites:
                sites[site].append(http - spdy)
            else:
                sites[site] = [http - spdy]

    s_sites = [sum(x)/len(x) for x in sites.values()]
    for time in sorted(s_sites):
        print time
