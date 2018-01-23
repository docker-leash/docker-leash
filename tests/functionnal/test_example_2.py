# vim:set ts=4 sw=4 et:
'''
ValidateExample2Functionnal
---------------------------
'''

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample2Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 2
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_2"
        application.config['GROUPS_FILE'] = example_dir + "/groups.yml"
        application.config['POLICIES_FILE'] = example_dir + "/policies.yml"

    def test_admin_1(self):
        """Admins can do everything: list containers
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_admin_2(self):
        """Admins can do everything: create containers
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_admin_3(self):
        """Admins can do everything: delete containers
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/abc123",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_authenticated_1(self):
        """Authenticated users are restricted to read-only actions: list containers
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_authenticated_2(self):
        """Authenticated users are restricted to read-only actions: create containers
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_authenticated_3(self):
        """Authenticated users are restricted to read-only actions: delete containers
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/abc123",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_anonymous_1(self):
        """Anonymous users cannot do anything: list containers
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_anonymous_2(self):
        """Anonymous users cannot do anything: create containers
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_anonymous_3(self):
        """Anonymous users cannot do anything: delete containers
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/abc123",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
