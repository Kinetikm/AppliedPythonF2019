#!/usr/bin/env python
# coding: utf-8
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleReqHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "Hello world!"
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, SimpleReqHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
