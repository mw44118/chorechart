# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import re
import urlparse

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
        and self.extract_chart_id(environ['PATH_INFO']):

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

class UpdateChart(ChartHandler):

    """

    Catches requests like POST /chart/99/fill_in_a_star, then does a
    redirect back to /chart/99.

    """

    path_info_pattern = re.compile(r'^/chart/(\d+)/([a-z_]+)$')

    allowed_actions = dict(
        fill_in_a_star=Chart.fill_in_a_star,
        reset_chart=Chart.reset_chart)

    @classmethod
    def extract_action(cls, path_info):

        match = cls.path_info_pattern.match(path_info)

        if match:
            return cls.allowed_actions.get(match.groups()[1])

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'POST' \
        and self.extract_chart_id(environ['PATH_INFO']):

            return self


    def __call__(self, environ, start_response):

        chart_id = self.extract_chart_id(environ['PATH_INFO'])

        chart = Chart.by_primary_key(self.dbconn, chart_id)

        action = self.extract_action(environ['PATH_INFO'])

        action(chart, self.dbconn)

        redirect_target = (
            '%s/chart/%d'
            % (
                self.config_wrapper.parsed_config['server']['host'],
                chart_id))

        start_response(
        '302 FOUND',
        [('Location', redirect_target)])

        return []

class NewChartForm(Handler):

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'GET' \
        and environ['PATH_INFO'] == '/new-chart':
            return self

    def __call__(self, environ, start_response):

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        t = self.templates.get_template('new-chart.html')

        return [t.render()]

class InsertChart(Handler):

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'POST' \
        and environ['PATH_INFO'] == '/new-chart':

            return self

    def __call__(self, environ, start_response):

        raw_post_data = environ['wsgi.input'].read(
            int(environ['CONTENT_LENGTH']))

        parsed_post_data = urlparse.parse_qs(raw_post_data)

        facebook_uid = self.facebook_uid_from_cookie(environ)

        try:

            chart = Chart.from_parsed_post_data(
                self.dbconn, facebook_uid, parsed_post_data)

            redirect_target = (
                '%s/chart/%s'
                % (self.config_wrapper.parsed_config['server']['host'],
                    chart.chart_id))

            start_response(
            '302 FOUND',
            [('Location', redirect_target)])

            return []

        except ValueError, ex:

            start_response(
                '200 OK',
                [('Content-Type', 'text/html; charset=utf-8')])

            message = ex.args[0]

            t = self.templates.get_template('new-chart-error.html')

            return [t.render(message=ex.args[0])]
