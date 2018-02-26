# vim:set ts=4 sw=4 et:
'''
BasicTests
----------
'''

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class BasicTests(LeashServerFunctionnalBaseTests):
    """Validate API endpoints
    """

    def test_main_page(self):
        """Validate access to the home page
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_activate_page(self):
        """Validate the most basic Plugin Activate Request
        """
        response = self.app.post('/Plugin.Activate')
        self.assertEqual(response.status_code, 200)

    def test_authz_req_page_1(self):
        """Validate the most basic Auth Request
        """
        payload = {
            "Host": "other01",
        }
        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)

    def test_authz_req_page_2(self):
        """An empty payload must raise an Exception
        """
        response = post(self.app, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_authz_res_page(self):
        """Validate access to the Auth Response
        """
        response = self.app.post('/AuthZPlugin.AuthZRes')
        self.assertEqual(response.status_code, 200)
