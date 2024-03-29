from __future__ import absolute_import

import sys
from os.path import dirname, join, isfile

from tornado.web import Application, StaticFileHandler, RequestHandler
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop

from streammania.handlers.shows import ShowsHandler
from streammania.handlers.auth import GoogleAuthHandler
from streammania.handlers.user import MeHandler
from streammania.models import Session, Base
from streammania.config import cookie_secret


here = dirname(__file__)
project_root = join(here, '..')
static_path = join(project_root, 'webapp/app')


define('port', default=8080, help='run on the given port', type=int)


class MainHandler(RequestHandler):
    def get(self):
        return self.render(static_path + '/index.html')


class StreamMania(Application):
    def __init__(self, dbsession=None, debug_mode=False):
        debug = debug_mode or isfile(join(project_root, 'debug'))
        handlers = [
            (r'/', MainHandler),
            (r'/api/auth/google/?', GoogleAuthHandler),
            (r'/api/me/?', MeHandler),
            (r'/api/shows/([a-zA-Z]{2})/(.*)/?', ShowsHandler),
            (r'/webapp/(.*)$', StaticFileHandler, {'path': static_path})
        ]
        if debug:
            from streammania.testing.handlers import testing_handlers
            handlers += testing_handlers
        settings = {
            'debug': debug,
            'cookie_secret': cookie_secret,
            'login_url': '/webapp/login/'
        }
        super(StreamMania, self).__init__(handlers, **settings)
        self.db = dbsession or Session
        Base.query = self.db.query_property()


def main():
    parse_command_line()
    app = StreamMania()
    app.listen(options.port, '0.0.0.0')
    print(
        'Starting StreamMania on http://localhost:{0}/'.format(options.port))
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
