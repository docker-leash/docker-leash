# vim:set ts=4 sw=4 et:
'''
BindMountsTests
----------------
'''

import unittest

from docker_leash.checks.bind_mounts import BindMounts
from docker_leash.exceptions import (InvalidRequestException,
                                     UnauthorizedException)
from docker_leash.payload import Payload

PAYLOAD_MINIMAL = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": []
        }
    },
}

PAYLOAD_FOO = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": [
                '/foo',
                '/foo/bar',
                '/foo/bar/team',
            ]
        }
    },
}

PAYLOAD_FOOBAR = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": [
                '/foo',
                '/foobar',
            ]
        }
    },
}

PAYLOAD_MANY = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": [
                '/',
                '/etc',
                '/foo',
                '/foo/lol',
                '/foo/foo',
                '/foo/bar',
                '/foo/bar/team',
                '/foo/bar/../baz',
                'foo',
            ]
        }
    },
}

PAYLOAD_USER = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": [
                '/home/someone',
            ]
        }
    },
}


class BindMountsTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.BindMounts`
    """

    def test_init(self):
        """Try init BindMounts with minimal informations
        """
        args = [
            '-/.*',
            '+/foo',
            '-/foo/.*',
            '+/foo/bar',
        ]

        with self.assertRaises(InvalidRequestException):
            BindMounts().run(None, Payload({}))

        with self.assertRaises(InvalidRequestException):
            BindMounts().run(args, Payload({}))

        BindMounts().run(args, Payload(PAYLOAD_MINIMAL))
        BindMounts().run(None, Payload(PAYLOAD_MINIMAL))

    @classmethod
    def test_valid_paths(cls):
        """Check valid paths
        """
        args = [
            '-/.*',
            '+/foo',
            '-/foo/.*',
            '+/foo/bar',
        ]

        BindMounts().run(args, Payload(PAYLOAD_FOO))

    def test_invalid_paths(self):
        """Check invalid paths
        """
        args = [
            '-/.*',
            '+/foo',
            '-/foo/.*',
            '+/foo/bar',
        ]

        with self.assertRaises(UnauthorizedException):
            BindMounts().run(args, Payload(PAYLOAD_MANY))

    @classmethod
    def test_invalid_rules_should_be_ignored(cls):
        """Unparsable rules are ignored
        """
        args = [
            '.*/.*',
            '%-/foo',
            '/foo/.*',
            '+/foo',
        ]

        BindMounts().run(args, Payload(PAYLOAD_FOO))

    @classmethod
    def test_directoy_names_starting_with(cls):
        """Check directory starting with
        """
        args = [
            '-/.*',
            '+/foo',
        ]

        BindMounts().run(args, Payload(PAYLOAD_FOO))

    def test_directoy_names_exact_match(self):
        """Check directory exact match
        """
        args = [
            '-/.*',
            '+/foo/',
        ]

        with self.assertRaises(UnauthorizedException):
            BindMounts().run(args, Payload(PAYLOAD_FOOBAR))

    @classmethod
    def test_directoy_names_containing_user(cls):
        """Check directory containing user
        """
        args = [
            '-/.*',
            '+/home/$USER',
        ]

        BindMounts().run(args, Payload(PAYLOAD_USER))
