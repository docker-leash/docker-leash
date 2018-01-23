# vim:set ts=4 sw=4 et:
'''
BindVolumesTestsFunctionnal
---------------------------
'''

import base64
import json

from docker_leash.leash_server import app

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class BindVolumesTestsFunctionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of :cls:`docker_leash.checks.BindVolumesTests`
    """

    def test_create_authenticated_valid(self):
        """Post a container create as authenticated
        """
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
            "UserAuthNMethod": "TLS",
            "RequestHeaders": {
                "Host": "wks01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_authenticated_invalid(self):
        """Post an invalid container create as authenticated
        """
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
            "UserAuthNMethod": "TLS",
            "RequestHeaders": {
                "Host": "wks01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_valid(self):
        """Post a container create as unauthenticated
        """
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
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_invalid(self):
        """Post an invalid container create as unauthenticated
        """
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
            "RequestHeaders": {
                "Host": "other01"
            }
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
