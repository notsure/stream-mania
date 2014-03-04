from __future__ import absolute_import

from tornado.web import RequestHandler

from streammania.models import User


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        openid = self.get_secure_cookie('usertoken')
        if isinstance(openid, bytes):
            openid = openid.decode('utf-8')
        user = User.query.filter_by(openid=openid).first()
        return user
