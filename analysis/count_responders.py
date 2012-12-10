#!/usr/bin/python
"""
Find which protocol was faster for each of the 2** sites.
"""
import sys
import json

if __name__ == '__main__':
    f = open(sys.argv[1])
    ips = set()
    uniqs = set()
    for line in f:
        blob = json.loads(line)
        ips.add(blob['ip'])
        uniqs.add(blob['uniq'])
    print 'ips:', len(ips)
    print 'ids:', len(uniqs)
