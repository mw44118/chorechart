# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import os
import re

import psycopg2
import yaml

import superfunchart

class Handler(object):

    def wants_to_handle(self, environ):
        return False

    def __init__(self, title, dbconn):
        self.title = title
        self.dbconn = dbconn

    def __call__(self, environ, start_response):

        start_response(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')])

        return [str('This is the base handler...')]


class Chart(Handler):

    """
    Handle requests like GET /chart/99.
    """

    def __wants_to_handle(self, environ):

        if environ['REQUEST_METHOD'] == 'GET' \
        and re.compile(r'^/chart/(\d+)$').match(environ['PATH_INFO']):

            return self

class Dispatcher(Handler):
    pass


class ConfigWrapper(object):

    def __init__(self, config):
        self.config = config

    @classmethod
    def from_yaml_file(cls, filename):
        """
        The file must be in the same folder as the superfunchart __init__.py
        file, because that's how I'll try to find it.
        """

        full_path = os.path.join(os.path.dirname(
            superfunchart.__file__), filename)

        config = yaml.load(open(full_path))

        return cls(config)

    def make_dbconn(self):

        return psycopg2.connect(
            port=self.config['database']['port'],
            database=self.config['database']['database'],
            host=self.config['database']['host'],
            user=self.config['database']['user'],
            password=self.config['database']['password'])


def make_app(path_to_config):

    """
    This builds and returns an object that gunicorn talks to.
    """

    dbconn =
