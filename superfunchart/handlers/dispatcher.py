# vim: set expandtab ts=4 sw=4 filetype=python:

import logging

from superfunchart.handlers import Handler

log = logging.getLogger('superfunchart.handlers.dispatcher')

class Dispatcher(Handler):

    """
    Handle requests by passing to the appropriate handler.
    """

    def __init__(self, title, dbconn):

        super(Dispatcher, self).__init__(title, dbconn)
        self.handlers = []
        self.error_page = self.templates.get_template('error.html')

    def __call__(self, environ, start_response):

        log.debug('dispatching %(REQUEST_METHOD)s %(PATH_INFO)s'
            % environ)

        try:

            for h in self.handlers:

                log.debug('Asking handler %s...' % h.title)

                if h.wants_to_handle(environ):

                    return h(environ, start_response)
                    self.dbconn.commit()

        except Exception, ex:
            log.debug('OH NOES')
            log.exception(ex)
            log.critical(environ)
            self.dbconn.rollback()

            start_response(
                '200 OK',
                [('Content-Type', 'text/html')],
                sys.exc_info())

            return [str(self.error_page.render(h=self))]
