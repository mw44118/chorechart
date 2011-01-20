# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import re

from superfunchart.handlers import Handler

log = logging.getLogger('superfunchart.handlers.chart')

class Chart(Handler):

    """
    Handle requests like GET /chart/99.
    """

    path_info_pattern = re.compile(r'^/chart/(\d+)$')

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'GET' \
        and self.path_info_pattern.match(environ['PATH_INFO']):

            return self

    def __call__(self, environ, start_response):

        t = self.templates.get_template('chart.html')

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        return [t.render()]
