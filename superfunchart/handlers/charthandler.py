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

        log.debug("inside wants_to_handle for %s" % self.title)

        log.debug(
            'request method: %(REQUEST_METHOD)s path info: %(PATH_INFO)s'
            % environ)

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

        log.debug("inside wants_to_handle for %s" % self.title)

        if environ['REQUEST_METHOD'] == 'POST' \
        and self.extract_chart_id(environ['PATH_INFO']):

            log.debug('yup!')

            return self

        else:

            log.debug('nope!')

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

