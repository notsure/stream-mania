
from tornado.web import HTTPError
from streammania.base import BaseHandler
from streammania.models import User


class MeHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            raise HTTPError(403)
        self.write({
            'status': 'success',
            'data': user.to_dict()
        })

    _user_properties = {'openid', 'email', 'first_name', 'last_name'}

    def post(self):
        if self.current_user and self.current_user.username:
            raise HTTPError(400)
        username = self.get_argument('username')
        user = User(username=username)
        for user_property in self._user_properties:
            value = self.get_secure_cookie(user_property).decode('utf-8')
            if not value:
                msg = "{} wasn't provided by the OpenID provider".format(
                    user_property)
                self.write({
                    'status': 'fail',
                    'data': {
                        user_property: msg
                    }
                })
                self.set_status(400)
                return
            setattr(user, user_property, value)
        self.db.add(user)
        self.db.commit()
        self.clear_all_cookies() # clear cookies set from openid provider
        self.set_secure_cookie('username', user.username)
