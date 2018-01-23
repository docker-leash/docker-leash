# vim:set ts=4 sw=4 et:
'''
ValidateExample3Functionnal
---------------------------
'''

import base64
import json

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample3Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 3
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_3"
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

    def test_user_1(self):
        """Users are restricted by container name: create containers valid name
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_2(self):
        """Users are restricted by container name: create containers $USER name
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=jre-bar",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_3(self):
        """Users are restricted by container name: create containers invalid name
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=something",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_4(self):
        """Users are restricted by container name: create image
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/build/something",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_5(self):
        """Users are restricted by container name: list image
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/images/json",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_6(self):
        """Users are restricted by container name: delete image
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/images/abc123",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_7(self):
        """Users are restricted by container name: delete container invalid
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/container/abc123",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_user_8(self):
        """Users are restricted by container name: delete container valid
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/container/foo-bar",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_user_9(self):
        """Users are restricted by container name: delete container $USER
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/container/jre-bar",
            "User": "jre",
            "RequestHeaders": {
                "Host": "srv01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

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
