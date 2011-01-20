# vim: set expandtab ts=4 sw=4 filetype=python:

import logging

from superfunchart.templates import make_jinja2_environment

log = logging.getLogger('superfunchart.handlers')

class Handler(object):

    def wants_to_handle(self, environ):
        return

    def __init__(self, title, dbconn):
        self.title = title
        self.dbconn = dbconn
        self.templates = make_jinja2_environment()

    def __call__(self, environ, start_response):

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        return [str('This is the base handler...')]

from superfunchart.handlers.charthandler import ChartHandler
from superfunchart.handlers.dispatcher import Dispatcher
