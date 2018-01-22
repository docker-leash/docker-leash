# vim:set ts=4 sw=4 et:
'''
LeashServerTests
----------------
'''

import base64
import json
import unittest

from docker_leash.leash_server import app

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class LeashServerTests(LeashServerFunctionnalBaseTests):
    """Functionnal validation of :cls:`docker_leash.LeashServer`
    """

    def test_ping(self):
        """The the ping endpoint
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/_ping"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_list_bad_method(self):
        """Check a wrong URI/Method combinaison
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/json"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_list_anonymous(self):
        """Check constainer list as anonymous
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_list_authenticated(self):
        """Check constainer list as authenticated
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "UserAuthNMethod": "TLS"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_anonymous(self):
        """Check create constainer as anonymous
        """
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_authenticated(self):
        """Check create constainer as authenticated
        """
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "mal",
            "UserAuthNMethod": "TLS"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))
