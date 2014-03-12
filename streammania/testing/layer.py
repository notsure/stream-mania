from __future__ import absolute_import

import multiprocessing

from tornado.ioloop import IOLoop


class TornadoLayer(object):

    __bases__ = ()
    __name__ = 'tornado'

    class TornadoProcess(multiprocessing.Process):

        def __init__(self, app, port, patches):
            super().__init__()
            self.app = app
            self.port = port
            self.patches = patches or []
            for patch in self.patches:
                patch.start()


        def terminate(self):
            for patch in self.patches:
                patch.stop()
            super().terminate()

        def run(self):
            self.app.listen(self.port)
            self.instance = IOLoop.instance()
            self.instance.start()

    def __init__(self, app, port, patches=None):
        self.server_process = self.TornadoProcess(app, port, patches)

    def setUp(self):
        self.server_process.start()

    def tearDown(self):
        self.server_process.terminate()
