# vim:set ts=4 sw=4 et:

import unittest

from app.leash_server import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_activate_page(self):
        response = self.app.post('/Plugin.Activate')
        self.assertEqual(response.status_code, 200)

    def test_authz_req_page(self):
        response = self.app.post('/AuthZPlugin.AuthZReq')
        self.assertEqual(response.status_code, 200)

    def test_authz_res_page(self):
        response = self.app.post('/AuthZPlugin.AuthZRes')
        self.assertEqual(response.status_code, 200)
