# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import logging.config
import os
import re

import psycopg2
import yaml

import superfunchart
from superfunchart.templates import make_jinja2_environment

log = logging.getLogger('superfunchart')

def load_logging_config():

    logging.config.fileConfig(os.path.join(
        os.path.dirname(__file__),
        'logging.cfg'))

from superfunchart import handlers

class ConfigWrapper(object):

    def __init__(self, parsed_config):
        self.parsed_config = parsed_config

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
            port=self.parsed_config['database']['port'],
            database=self.parsed_config['database']['database'],
            host=self.parsed_config['database']['host'],
            user=self.parsed_config['database']['user'],
            password=self.parsed_config['database']['password'])

    @property
    def app_id(self):
        return self.parsed_config['facebook']['app_id']

def make_app(path_to_config):

    """
    This builds and returns an object that gunicorn talks to.
    """

    load_logging_config()

    log.debug('making app...')

    cw = ConfigWrapper.from_yaml_file(path_to_config)

    log.debug('yaml!')

    dbconn = cw.make_dbconn()

    log.debug('dbconn!')

    app = handlers.Dispatcher(title='Dispatcher', config_wrapper=cw, dbconn=dbconn)

    log.debug('dispatcher!')

    app.handlers.append(
        handlers.ChartHandler(
            title='GET /chart/{chart_id}',
            config_wrapper=cw,
            dbconn=dbconn))

    log.debug('chart GET handler!')

    app.handlers.append(
        handlers.UpdateChart(
            title='POST /chart/{chart_id}/{action}',
            config_wrapper=cw,
            dbconn=dbconn))

    log.debug('chart POST handler!')

    app.handlers.append(
        handlers.NewChartForm(
            title='GET /new-chart',
            config_wrapper=cw,
            dbconn=dbconn))

    log.debug('GET /new-chart')

    app.handlers.append(
        handlers.InsertChart(
            title='POST /new-chart',
            config_wrapper=cw,
            dbconn=dbconn))

    log.debug('POST /new-chart')

    app.handlers.append(
        handlers.SplashPage(
            title='GET /',
            config_wrapper=cw,
            dbconn=dbconn))

    log.debug('GET /')


    log.debug('app all set up!')

    return app
