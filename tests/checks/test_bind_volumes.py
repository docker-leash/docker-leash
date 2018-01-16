# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.bind_volumes import BindVolumes
from docker_leash.exceptions import UnauthorizedException
from docker_leash.payload import Payload

payload_minimal = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": []
        }
    }
}

payload_foo = {
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
    }
}

payload_foobar = {
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
    }
}

payload_many = {
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
    }
}

class BindVolumesTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        args = [
            '-/*',
            '+/foo',
            '-/foo/*',
            '+/foo/bar',
        ]

        BindVolumes().run(None, Payload({}))
        BindVolumes().run(args, Payload({}))
        BindVolumes().run(args, Payload(payload_minimal))
        BindVolumes().run(None, Payload(payload_minimal))

    @classmethod
    def test_valid_paths(cls):
        args = [
            '-/*',
            '+/foo',
            '-/foo/*',
            '+/foo/bar',
        ]

        BindVolumes().run(args, Payload(payload_foo))

    def test_invalid_paths(self):
        args = [
            '-/*',
            '+/foo',
            '-/foo/*',
            '+/foo/bar',
        ]

        with self.assertRaises(UnauthorizedException):
            BindVolumes().run(args, Payload(payload_many))

    @classmethod
    def test_invalid_rules_should_be_ignored(cls):
        args = [
            '*/*',
            '%-/foo',
            '/foo/*',
            '+/foo',
        ]

        BindVolumes().run(args, Payload(payload_foo))

    @classmethod
    def test_directoy_names_starting_with(cls):
        args = [
            '-/*',
            '+/foo',
        ]

        BindVolumes().run(args, Payload(payload_foo))

    def test_directoy_names_exact_match(self):
        args = [
            '-/*',
            '+/foo/',
        ]

        with self.assertRaises(UnauthorizedException):
            BindVolumes().run(args, Payload(payload_foobar))
