
from tornado.web import RequestHandler


class FakeAuthHandler(RequestHandler):
    def post(self):
        self.set_secure_cookie('username', 'hoschi')
        return self.write({
            'status': 'success',
            'data': None
        })

    def delete(self):
        self.clear_all_cookies()


class FakeOpenIDHandler(RequestHandler):
    def post(self):
        self.set_secure_cookie('openid', 'openid_hoschi')
        self.set_secure_cookie('email', 'hoschi@galoschi.at')
        self.set_secure_cookie('first_name', 'Hoschi')
        self.set_secure_cookie('last_name', 'Galoschi')


testing_handlers = [
    (r'/__debug/api/auth/?', FakeAuthHandler),
    (r'/__debug/api/auth/google/?', FakeOpenIDHandler)
]
