# vim:set ts=4 sw=4 et:
'''
ValidateExample4Functionnal
---------------------------
'''

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample4Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 4
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_4"
        application.config['GROUPS_FILE'] = example_dir + "/groups.yml"
        application.config['POLICIES_FILE'] = example_dir + "/policies.yml"

    def test_servers_1(self):
        """Servers are restricted to admin only: admin
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

    def test_servers_2(self):
        """Servers are restricted to admin only: user
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
        self.assertFalse(is_success(response))

    def test_servers_3(self):
        """Servers are restricted to admin only: user not from any group
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "vol",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_servers_4(self):
        """Servers are restricted to admin only: anonymous
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

    def test_other_1(self):
        """All other hosts are open to group, else deny: admin
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_2(self):
        """All other hosts are open to group, else deny: user from any group
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "jre",
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_other_3(self):
        """All other hosts are open to group, else deny: user not from group
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "vol",
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_4(self):
        """All other hosts are open to group, else deny: anonymous
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
