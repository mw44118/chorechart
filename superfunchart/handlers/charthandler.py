# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import re

from superfunchart.handlers import Handler

from superfunchart.datamodel import Chart

log = logging.getLogger('superfunchart.handlers.charthandler')

class ChartHandler(Handler):

    """
    Handle requests like GET /chart/99.
    """

    path_info_pattern = re.compile(r'^/chart/(\d+)$')

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'GET' \
        and self.path_info_pattern.match(environ['PATH_INFO']):

            return self

    @classmethod
    def extract_chart_id(cls, path_info):

        match = cls.path_info_pattern.match(path_info)

        if match:
            return int(match.groups()[0])


    def __call__(self, environ, start_response):

        chart_id = self.extract_chart_id(environ['PATH_INFO'])

        chart = Chart.by_primary_key(self.dbconn, chart_id)

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        t = self.templates.get_template('chart.html')

        return [t.render(chart=chart)]
