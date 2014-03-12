import unittest
import doctest
import socket
import requests
import json

from os.path import dirname, join
from crate.testing.layer import CrateLayer
from crate.client import connect
from lovely.testlayers.layer import CascadedLayer

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from streammania.app import StreamMania
from streammania.testing.layer import TornadoLayer
from streammania.testing.tvdb import tvdb_mock

here = dirname(__file__)
crate_path = join(here, '../parts/crate')
crate_exec = join(crate_path, 'bin/crate')


def printjson(jsonstr):
    d = json.loads(jsonstr.decode('utf-8'))
    print(json.dumps(d, indent=4, sort_keys=True))


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


engine = create_engine('crate://localhost:{}'.format(crate_port))
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))
app = StreamMania(dbsession=Session, debug_mode=True)
tornado_layer = TornadoLayer(app, tornado_port, patches=[tvdb_mock])

crate_host = '127.0.0.1:{port}'.format(port=crate_port)
crate_uri = 'http://{0}'.format(crate_host)


layer = CascadedLayer('all', crate_layer, tornado_layer)


class WrappedSession():
    def __init__(self, uri, session, method=None):
        self.uri = uri
        self.session = session
        self.method = method

    def login(self):
        self.session.post('{}/__debug/api/auth/'.format(self.uri))

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
    test.globs['printjson'] = printjson
    test.globs['client'] = WrappedSession(tornado_uri, requests.session())

    conn = connect(crate_host)
    c = conn.cursor()
    with open(join(here, 'sql/users.sql')) as f:
        create_table = f.read()
        c.execute(create_table)
    sample_users = join(here, 'testing/sample_data/users.json')
    c.execute("copy users from '{0}'".format(sample_users))
    c.execute("refresh table users")


def tearDown(test):
    conn = connect(crate_host)
    c = conn.cursor()
    c.execute('drop table users')


def test_suite():
    suite = unittest.TestSuite()
    flags = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    testfiles = ('shows', 'me')
    testfiles = ('../docs/{}.rst'.format(f) for f in testfiles)
    for testfile in testfiles:
        s = doctest.DocFileSuite(testfile,
                                 setUp=setUpWithCrate,
                                 tearDown=tearDown,
                                 optionflags=flags)
        s.layer = layer
        suite.addTest(s)
    return suite
