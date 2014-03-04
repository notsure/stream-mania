from __future__ import absolute_import

import sys
from os.path import dirname, join, isfile

from tornado.web import Application, StaticFileHandler, RequestHandler
from tornado.options import define, options, parse_command_line
from tornado.ioloop import IOLoop

from streammania.handlers import (
    GoogleAuthHandler,
    ProfileHandler,
    ShowsHandler
)
from streammania.models import Session, Base


here = dirname(__file__)
project_root = join(here, '..')


define('port', default=8080, help='run on the given port', type=int)


class MainHandler(RequestHandler):
    def get(self):
        return self.redirect('/static/index.html')


class StreamMania(Application):
    def __init__(self):
        static_path = join(project_root, 'webapp/app')
        handlers = [
            (r'/', MainHandler),
            (r'/api/auth/google/?', GoogleAuthHandler),
            (r'/api/me/profile/?', ProfileHandler),
            (r'/api/shows/?', ShowsHandler),
            (r'/static/(.*)$', StaticFileHandler, {'path': static_path})
        ]
        settings = {
            'debug': isfile(join(project_root, 'debug')),
            'login_url': '/api/auth/google/'
        }
        super(StreamMania, self).__init__(handlers, **settings)
        self.db = Session
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
