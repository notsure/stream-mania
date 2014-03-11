import tornado.auth
from tornado.web import asynchronous

from streammania.models import User
from streammania.base import BaseHandler


class GoogleAuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @asynchronous
    def get(self):
        if self.get_argument('openid.mode', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'Google auth failed')
        dbuser = User.query.filter_by(openid=user['claimed_id']).first()
        if dbuser:
            dbuser.first_name = user['first_name']
            dbuser.last_name = user['last_name']
            dbuser.email = user['email']
        else:
            dbuser = User(first_name=user['first_name'],
                          last_name=user['last_name'],
                          email=user['email'],
                          openid=user['claimed_id'])
            self.db.add(dbuser)
        self.write({
            'status': 'success',
            'data': None
        })
        self.db.commit()
        self.set_secure_cookie('usertoken', dbuser.openid)
        self.finish()
