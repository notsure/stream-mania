
from tornado.web import RequestHandler


class FakeAuthHandler(RequestHandler):
    def post(self):
        self.set_secure_cookie('usertoken', 'openid_hoschi')
        return self.write({
            'status': 'success',
            'data': None
        })


testing_handlers = [
    (r'/__debug/api/auth/?', FakeAuthHandler)
]
