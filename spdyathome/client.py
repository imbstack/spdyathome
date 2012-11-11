"""
Client to run the tests
"""
import sys
from thor import HttpClient
from thor.events import on
from thor.loop import stop, run


if __name__ == '__main__':
    httpclient = HttpClient()
    httpexch = httpclient.exchange()

    @on(httpexch)
    def response_start(status, phrase, headers):
        print status
        print phrase

    httpexch.on('response_body', sys.stdout.write)

    @on(httpexch)
    def response_done(trailers):
        print
        stop()

    httpexch.request_start('GET', 'http://localhost:38091/hello', [])
    httpexch.request_done([])
    run()
