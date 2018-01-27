# vim:set ts=4 sw=4 et:
'''
Issue56Functionnal
------------------
'''

import os

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class Issue56Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of issue #56
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        application.config['GROUPS_FILE'] = dir_path + "/mocked_configs/issue_56/groups.yml"
        application.config['POLICIES_FILE'] = dir_path + "/mocked_configs/issue_56/policies.yml"

    def test_user_1(self):
        """Users have restricted access to containers: write valid
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_2(self):
        """Users have restricted access to containers: write invalid
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=blabla",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_3(self):
        """Everyone should have readonly: user read valid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/foo-bar/json",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_4(self):
        """Everyone should have readonly: user read invalid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/blabla/json",
            "User": "mal",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_anonymous_1(self):
        """Users have restricted access to containers: write valid
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_anonymous_2(self):
        """Users have restricted access to containers: write invalid
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=blabla",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_anonymous_3(self):
        """Everyone should have readonly: anonymous read valid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/foo-bar/json",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_anonymous_4(self):
        """Everyone should have readonly: anonymous read invalid
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/blabla/json",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        print response.data
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
