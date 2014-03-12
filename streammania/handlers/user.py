
from tornado.web import HTTPError
from streammania.base import BaseHandler


class MeHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            raise HTTPError(405)
        self.write({
            'status': 'success',
            'data': user.to_dict()
        })
