from setuptools import find_packages, setup

setup(

    name='SuperFunChart',

    version='0.0.1',    # This version number uses semantic versioning.
                        # Read http://semer.org for an explanation.

    description="My AGI hackday 2011 project",

    package=find_packages(),

    install_requires=[
        'clepy',
        'coverage',
        'gunicorn',
        'IPython',
        'pitz',
        'PyYAML',
        'jinja2',
        'mock',
        'nose',
        'psycopg2',
    ],

)
