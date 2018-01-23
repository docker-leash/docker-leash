# vim:set ts=4 sw=4 et:
'''
Issue30Functionnal
------------------
'''

import os

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class Issue30Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of issue #30
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        application.config['GROUPS_FILE'] = dir_path + "/mocked_configs/issue_30/groups.yml"
        application.config['POLICIES_FILE'] = dir_path + "/mocked_configs/issue_30/policies.yml"

    def test_admin_1(self):
        """Admin have full access: read
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
        """Admin have full access: write
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

    def test_user_1(self):
        """Users can manage containers whose name start by user name: list
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "cru",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_2(self):
        """Users can manage containers whose name start by user name: create valid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json?name=cru-bar",
            "User": "cru",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_3(self):
        """Users can manage containers whose name start by user name: create invalid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json?name=foo-bar",
            "User": "cru",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_4(self):
        """Users can manage containers whose name start by user name: delete valid
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/cru-bar",
            "User": "cru",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        print response.data
        self.assertTrue(is_success(response))

    def test_user_5(self):
        """Users can manage containers whose name start by user name: delete invalid
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/foo-bar",
            "User": "cru",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
