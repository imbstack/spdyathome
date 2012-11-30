"""
Client to run the tests.  Uses thor for both SPDY and HTTP clients
"""
import json
import time
import argparse
import random
import datetime
import sys
import socket
from . import conf
from thor import HttpClient
from thor import SpdyClient
from thor.loop import stop, run


def get_args():
    parser = argparse.ArgumentParser(
            description='Run HTTP and SPDY clients for test.')
    return parser.parse_args()


def hello(host):
    resp = {'text': '', 'sitelist': [], 'ip': ''}

    def hello_start(status, phrase, headers):
        if status == '200':
            print 'Connection Successful!\nDownloading sitelist.'

    def hello_body(chunk):
        resp['text'] += chunk

    def hello_stop(trailers):
        dct = json.loads(resp['text'])
        resp['sitelist'] = dct['sitelist']
        resp['ip'] = dct['ip']
        stop()

    def hello_err(err):
        print 'Connection could not be completed...'
        stop()
        exit()

    httpclient = HttpClient()
    httpclient.connect_timeout = 5
    hello = httpclient.exchange()
    hello.on('response_start', hello_start)
    hello.on('response_body', hello_body)
    hello.on('response_done', hello_stop)
    hello.on('error', hello_err)
    uri = host + '/hello'
    hello.request_start('GET', uri, [])
    hello.request_done([])
    run()
    return resp


def collect(host, data):

    def collect_start(status, phrase, headers):
        if status != '200':
            print 'Uploading data...'

    def collect_body(chunk):
        pass

    def collect_stop(trailers):
        stop()

    httpclient = HttpClient()
    collect = httpclient.exchange()
    collect.on('response_start', collect_start)
    collect.on('response_body', collect_body)
    collect.on('response_done', collect_stop)
    collect.request_start('POST', host, [])
    collect.request_body(data)
    collect.request_done([])
    run()
    return "Upload Complete"


def http_siteget(http1, http2, site):
    resp = {'text': '', 'assetlist': []}

    def site_start(status, phrase, headers):
        if status != '200':
            print 'Connection Failed: ' + site

    def site_body(chunk):
        resp['text'] += chunk

    def site_stop(trailers):
        assetlist = json.loads(resp['text'])['list']
        for asset in assetlist:
            http_assetget(http1, http2, asset, httpclient)
        print
        stop()

    t0 = time.time()
    print 'HTTP:',
    httpclient = HttpClient()
    get = httpclient.exchange()
    get.on('response_start', site_start)
    get.on('response_body', site_body)
    get.on('response_done', site_stop)
    uri = http1 + '/site/' + str(site)
    get.request_start('GET', uri, [])
    get.request_done([])
    run()
    return time.time() - t0


def http_assetget(http1, http2, asset, httpclient):
    sys.stdout.write('.')
    sys.stdout.flush()
    resp = {'text': ''}

    def asset_start(status, phrase, headers):
        if status != '200':
            print 'Connection Failed: ' + asset
            print status
            print phrase

    def asset_body(chunk):
        resp['text'] += chunk

    def asset_stop(trailers):
        pass

    get = httpclient.exchange()
    get.on('response_start', asset_start)
    get.on('response_body', asset_body)
    get.on('response_done', asset_stop)
    parts = asset.split('/')
    if parts[0] == 'host1':
        uri = http1 + '/asset/' + parts[1]
    else:
        uri = http2 + '/asset/' + parts[1]
    get.request_start('GET', uri, [])
    get.request_done([])


def spdy_siteget(spdy1, spdy2, site):
    resp = {'text': '', 'assetlist': []}

    def site_start(status, phrase, headers):
        if status != '200':
            print 'Connection Failed: ' + site

    def site_body(chunk):
        resp['text'] += chunk

    def site_stop(trailers):
        assetlist = json.loads(resp['text'])['list']
        for asset in assetlist:
            spdy_assetget(spdy1, spdy2, asset, spdyclient)
        print
        stop()

    t0 = time.time()
    print 'SPDY:',
    spdyclient = SpdyClient()
    get = spdyclient.exchange()
    uri = spdy1 + '/site/' + str(site)
    stream = get.request_start('GET', uri, [])
    get._streams[stream].on('response_start', site_start)
    get._streams[stream].on('response_body', site_body)
    get._streams[stream].on('response_done', site_stop)
    get._streams[stream].request_done(stream, [])
    run()
    return time.time() - t0


def spdy_assetget(spdy1, spdy2, asset, spdyclient):
    sys.stdout.write('.')
    sys.stdout.flush()
    resp = {'text': ''}

    def asset_start(status, phrase, headers):
        if status != '200':
            print 'Connection Failed: ' + asset

    def asset_body(chunk):
        resp['text'] += chunk

    def asset_stop(trailers):
        pass

    get = spdyclient.exchange()
    parts = asset.split('/')
    if parts[0] == 'host1':
        uri = str(spdy1 + '/asset/' + parts[1])
    else:
        uri = str(spdy2 + '/asset/' + parts[1])
    stream = get.request_start('GET', uri, [])
    get._streams[stream].on('response_start', asset_start)
    get._streams[stream].on('response_body', asset_body)
    get._streams[stream].on('response_done', asset_stop)
    get._streams[stream].request_done(stream, [])


def main():
    args = get_args()

    mainhost_http = conf.mainhost + ':' + str(conf.http_port)
    mainhost_spdy = conf.mainhost + ':' + str(conf.spdy_port)
    secondhost_http = conf.secondhost + ':' + str(conf.http_port)
    secondhost_spdy = conf.secondhost + ':' + str(conf.spdy_port)
    mainhost_collect = conf.mainhost + ':' + str(conf.capture_port)

    hello_resp = hello(mainhost_http)
    sites = hello_resp['sitelist']
    times = {'ip': hello_resp['ip'], 'uniq': hash(socket.gethostname())}
    random.shuffle(sites)
    for i,site in enumerate(sites):
        # Randomize ordering of HTTP and SPDY transactions
        print 'DEBUG', site
        print 'Working on site %d/%d [%s] '%(i, len(sites), str(datetime.datetime.now()))
        http_delta = {}
        spdy_delta = {}
        if random.random() > 0.5:
            http_delta['order'] = 0
            spdy_delta['order'] = 1
            try:
                http_delta['time'] = http_siteget(mainhost_http,
                        secondhost_http,
                        site)
            except:
                stop()
                http_delta['time'] = -1
            try:
                spdy_delta['time'] = spdy_siteget(mainhost_spdy,
                        secondhost_spdy,
                        site)
            except:
                stop()
                spdy_delta['time'] = -1
        else:
            http_delta['order'] = 1
            spdy_delta['order'] = 0
            try:
                spdy_delta['time'] = spdy_siteget(mainhost_spdy,
                        secondhost_spdy,
                        site)
            except:
                stop()
                spdy_delta['time'] = -1
            try:
                http_delta['time'] = http_siteget(mainhost_http,
                        secondhost_http,
                        site)
            except:
                stop()
                http_delta['time'] = -1
        times[site] = {'order': i, 'timestamp': str(datetime.datetime.now())}
        times[site]['http'] = http_delta
        times[site]['spdy'] = spdy_delta
        time.sleep(1)

    print 'Testing complete!'
    result = collect(mainhost_collect, json.dumps(times))
    print result
    stop()


if __name__ == '__main__':
    main()
