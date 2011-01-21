# vim: set expandtab ts=4 sw=4 filetype=python:

import Cookie
import logging
import urlparse

from superfunchart.templates import make_jinja2_environment

log = logging.getLogger('superfunchart.handlers')

class Handler(object):

    def wants_to_handle(self, environ):
        return

    def __init__(self, title, config_wrapper, dbconn):
        self.title = title
        self.config_wrapper = config_wrapper
        self.dbconn = dbconn

        self.templates = make_jinja2_environment()

    def __call__(self, environ, start_response):

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        return [str('This is the base handler...')]

    @staticmethod
    def is_an_ajax_request(environ):
        return False

    def facebook_uid_from_cookie(self, environ):

        """
        If I can dig up a facebook UID, I'll return it.
        """

        if 'HTTP_COOKIE' not in environ:
            return

        k = 'fbs_%s' % self.config_wrapper.app_id

        c = Cookie.SimpleCookie(environ['HTTP_COOKIE'])

        if k not in c:
            return

        parsed_cookie_guts = urlparse.parse_qs(c[k].value)

        if 'uid' not in parsed_cookie_guts:
            return

        return parsed_cookie_guts['uid'][0]

from superfunchart.handlers.charthandler import ChartHandler, \
NewChartForm, UpdateChart, InsertChart

from superfunchart.handlers.dispatcher import Dispatcher

from superfunchart.handlers.splashpage import SplashPage

