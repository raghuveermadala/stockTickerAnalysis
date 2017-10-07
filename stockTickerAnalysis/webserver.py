#!/usr/bin/python3

import config

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from api import app

port = config.tornado_port

print("Starting ... go get that alpha!")
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port)
IOLoop.instance().start()
