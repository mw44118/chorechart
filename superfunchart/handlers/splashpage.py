# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import re
import urlparse

from superfunchart.datamodel import Chart
from superfunchart.handlers import Handler

log = logging.getLogger('superfunchart.handlers.splashpage')

class SplashPage(Handler):

    def wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'GET' \
        and environ['PATH_INFO'] == '/':

            return self

    def __call__(self, environ, start_response):

        facebook_uid = self.facebook_uid_from_cookie(environ)

        if facebook_uid:

            my_charts = Chart.my_charts(self.dbconn, facebook_uid)

            start_response(
                '200 OK',
                [('Content-Type', 'text/html; charset=utf-8')])

            t = self.templates.get_template('my-charts.html')

            return [t.render(
                app_id=self.config_wrapper.app_id,
                my_charts=my_charts)]

        else:

            start_response(
                '200 OK',
                [('Content-Type', 'text/html; charset=utf-8')])

            t = self.templates.get_template('splashpage.html')

            return [t.render(
                app_id=self.config_wrapper.app_id)]
