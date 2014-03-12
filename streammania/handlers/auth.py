import tornado.auth
from tornado.web import asynchronous

from streammania.models import User
from streammania.base import BaseHandler


class GoogleAuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @asynchronous
    def get(self):
        user = self.get_current_user()
        if user and not user.username:
            self.redirect('/webapp/register')
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
            self.set_secure_cookie('username', dbuser.username)
            self.db.commit()
        else:
            self.set_secure_cookie('openid', user['claimed_id'])
            self.set_secure_cookie('email', user['email'])
            self.set_secure_cookie('first_name', user['first_name'])
            self.set_secure_cookie('last_name', user['last_name'])
        self.write(dict(status='success', data=None))
        self.finish()
