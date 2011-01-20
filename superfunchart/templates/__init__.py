# vim: set expandtab ts=4 sw=4 filetype=python:

import os

import jinja2

def make_jinja2_environment():

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)))
