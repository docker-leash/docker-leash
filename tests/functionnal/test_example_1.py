# vim:set ts=4 sw=4 et:
'''
ValidateExample1Functionnal
---------------------------
'''

import base64
import json

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample1Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 1
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_1"
        application.config['GROUPS_FILE'] = example_dir + "/groups.yml"
        application.config['POLICIES_FILE'] = example_dir + "/policies.yml"

    def test_list_as_anonymous(self):
        """List containers as anonymous
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_list_as_authenticated(self):
        """List containers as authenticated
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_as_anonymous(self):
        """Create a container as anonymous
        """
        payload = {
            "RequestBody": base64.b64encode(json.dumps({})),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_as_authenticated(self):
        """Post a container create as authenticated
        """
        payload = {
            "RequestBody": base64.b64encode(json.dumps({})),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "mal",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))
