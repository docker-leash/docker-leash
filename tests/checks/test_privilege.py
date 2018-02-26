# vim:set ts=4 sw=4 et:
'''
PrivilegedTests
-------------
'''

import unittest

from docker_leash.checks.privileged import Privileged
from docker_leash.config import Config
from docker_leash.exceptions import (InvalidRequestException,
                                     UnauthorizedException)
from docker_leash.payload import Payload

MOCKED_WITHOUT_PRIVILEGED = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {"foo": "bar"},
}

MOCKED_PRIVILEGED_FALSE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "HostConfig": False,
        },
    },
}

MOCKED_PRIVILEGED_TRUE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Privileged": True,
        },
    },
}


POLICIES = [
    {
        "description": "Priviled flag must be `off`.",
        "hosts": [r"+.*"],
        "default": "Allow",
        "policies": [
            {
                "members": ["all"],
                "rules": {
                    "any": {
                        "Privileged": None
                    }
                }
            },
        ],
    },
]

GROUPS = {"all": "*"}


class PrivilegedTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.Privileged`
    """

    @staticmethod
    def test_without_flag():
        """Validate Privileged whithout flag
        """
        config = Config(policies=POLICIES, groups=GROUPS)

        privileged = Privileged()
        privileged.run(config, Payload(MOCKED_WITHOUT_PRIVILEGED))

    @staticmethod
    def test_with_flag_false():
        """Validate Privileged with flag as false
        """
        config = Config(policies=POLICIES, groups=GROUPS)

        privileged = Privileged()
        privileged.run(config, Payload(MOCKED_PRIVILEGED_FALSE))

    def test_with_flag_true(self):
        """Validate Privileged with flag as true
        """
        config = Config(policies=POLICIES, groups=GROUPS)

        privileged = Privileged()
        with self.assertRaises(UnauthorizedException):
            privileged.run(config, Payload(MOCKED_PRIVILEGED_TRUE))
