# vim:set ts=4 sw=4 et:

import base64
import json
import unittest

from docker_leash.leash_server import app

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class BindVolumesTestsFunctionnal(LeashServerFunctionnalBaseTests):

    def test_create_authenticated_valid(self):
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
            "HostConfig": {
                "Binds": [
                    "/0:/mnt/0:rw"
                ]
            },
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "User": "jre",
            "UserAuthNMethod": "TLS"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_authenticated_invalid(self):
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
            "HostConfig": {
                "Binds": [
                    "/etc:/mnt/etc:rw"
                ]
            },
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "User": "jre",
            "UserAuthNMethod": "TLS"
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_valid(self):
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
            "HostConfig": {
                "Binds": [
                    "/0:/mnt/0:rw"
                ]
            },
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_invalid(self):
        request = {
            "Cmd": [
                "date"
            ],
            "Image": "bash:4.4",
            "HostConfig": {
                "Binds": [
                    "/etc:/mnt/etc:rw"
                ]
            },
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
