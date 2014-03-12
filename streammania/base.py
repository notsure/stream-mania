from __future__ import absolute_import

from tornado.web import RequestHandler

from streammania.models import User


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        if not username:
            return None
        if isinstance(username, bytes):
            username = username.decode('utf-8')
        user = User.query.filter_by(username=username).first()
        return user
