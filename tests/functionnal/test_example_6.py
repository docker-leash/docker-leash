# vim:set ts=4 sw=4 et:
'''
ValidateExample6Functionnal
---------------------------
'''

import base64
import json

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample6Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 6
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_6"
        application.config['GROUPS_FILE'] = example_dir + "/groups.yml"
        application.config['POLICIES_FILE'] = example_dir + "/policies.yml"

    def test_no_effect_on_some_endpoints(self):
        """Module has no effect on some endpoints
        """
        payload = {
            "User": "mal",
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "Host": "host01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))


    def test_use_default_image_user(self):
        """Use the default`run as` from image
        """
        payload = {
            "User": "foobar",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {
                "User": "",
            },
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

        payload = {
            "User": "foobar",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {},
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))


    def test_run_as_user(self):
        """Run as $USER
        """
        payload = {
            "User": "foobar",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {
                "User": "foobar",
            },
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))


    def test_run_as_other_user(self):
        """Run as other user: forbidden
        """
        payload = {
            "User": "foobar",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {
                "User": "other",
            },
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))


    def test_run_as_nobody(self):
        """Run as nobody
        """
        payload = {
            "User": "foobar",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {
                "User": "nobody",
            },
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))


    def test_run_as_nobody_but_unauthenticated(self):
        """Unauthenticated user run as nobody
        """
        payload = {
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {
                "User": "nobody",
            },
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))
