# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.leash_server import app


class LeashServerFunctionnalBaseTests(unittest.TestCase):

    def setUp(self):
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass
