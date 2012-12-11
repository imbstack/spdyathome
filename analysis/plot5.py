#!/usr/bin/python
"""
5. whisker plot for any multiple responders
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    responders = {}
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
        if blob['ip'] in responders:
            responders[blob['ip']].append(sum(sd)/len(sd))
        else:
            responders[blob['ip']] = [sum(sd)/len(sd)]

    i = 1
    for x in responders.values():
        if len(x) < 5:
            continue
        print i,
        print min(x),
        print x[int(len(x)/4)],
        print sum(x)/len(x),
        print x[3*int(len(x)/4)],
        print max(x)
        i += 1
