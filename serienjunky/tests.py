import unittest
import doctest
import socket
import requests

from os.path import dirname, join
from crate.testing.layer import CrateLayer
from lovely.testlayers.layer import CascadedLayer
from serienjunky.testing.layer import TornadoLayer


here = dirname(__file__)
crate_path = join(here, '../parts/crate')
crate_exec = join(crate_path, 'bin/crate')


def get_rnd_port():
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]


crate_port = get_rnd_port()
crate_transport = get_rnd_port()
crate_layer = CrateLayer('crate',
                         crate_home=crate_path,
                         crate_exec=crate_exec,
                         port=crate_port,
                         transport_port=crate_transport)

tornado_port = get_rnd_port()
tornado_host = 'localhost:{port}'.format(port=tornado_port)
tornado_uri = 'http://{host}'.format(host=tornado_host)
tornado_layer = TornadoLayer(tornado_port)

crate_host = '127.0.0.1:{port}'.format(port=crate_port)
crate_uri = 'http://{0}'.format(crate_host)


#layer = CascadedLayer('all', crate_layer, tornado_layer)
layer = tornado_layer


class WrappedSession():
    def __init__(self, uri, session, method=None):
        self.uri = uri
        self.session = session
        self.method = method

    def __getattr__(self, attr):
        return WrappedSession(self.uri, self.session, attr)

    def __call__(self, *args, **kwargs):
        method = getattr(self.session, self.method)
        url = args[0]
        if url.startswith('/'):
            url = url[1:]
        url = '{0}/{1}'.format(self.uri, url)
        return method(url, **kwargs)


def setUpWithCrate(test):
    test.globs['client'] = WrappedSession(tornado_uri, requests.session())


def test_suite():
    suite = unittest.TestSuite()
    s = doctest.DocFileSuite('../docs/auth.rst', setUp=setUpWithCrate)
    s.layer = layer
    suite.addTest(s)
    return suite
