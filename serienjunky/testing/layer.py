from __future__ import absolute_import

import multiprocessing

from tornado.ioloop import IOLoop
from serienjunky.app import SerienJunky


class TornadoLayer(object):

    __bases__ = ()
    __name__ = 'tornado'

    class TornadoProcess(multiprocessing.Process):

        def __init__(self, port):
            super().__init__()
            self.port = port

        def run(self):
            app = SerienJunky()
            app.listen(self.port)
            self.instance = IOLoop.instance()
            self.instance.start()

    def __init__(self, port):
        self.server_process = self.TornadoProcess(port)

    def setUp(self):
        self.server_process.start()

    def tearDown(self):
        self.server_process.terminate()
