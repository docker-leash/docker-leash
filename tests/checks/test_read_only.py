# vim:set ts=4 sw=4 et:
'''
ReadOnlyTests
-------------
'''

import unittest

from docker_leash.checks.read_only import ReadOnly
from docker_leash.config import Config
from docker_leash.exceptions import (InvalidRequestException,
                                     UnauthorizedException)
from docker_leash.payload import Payload

MOCKED_GET_BODY = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.32/containers/json",
    "RequestHeaders": {
        "Host": "other01"
    },
}

MOCKED_HEAD_BODY = {
    "User": "someone",
    "RequestMethod": "HEAD",
    "RequestUri": "/v1.32/containers/abc123/archive",
    "RequestHeaders": {
        "Host": "other01"
    },
}

MOCKED_POST_BODY = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {
        "Host": "other01"
    },
}

MOCKED_DELETE_BODY = {
    "User": "someone",
    "RequestMethod": "DELETE",
    "RequestUri": "/v1.32/containers/abc123",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {
        "Host": "other01"
    },
}

MOCKED_PUT_BODY = {
    "User": "someone",
    "RequestMethod": "PUT",
    "RequestUri": "/v1.32/containers/abc123/archive",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {
        "Host": "other01"
    },
}


class ReadOnlyTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.ReadOnly`
    """

    @staticmethod
    def test_read_operation():
        """Validate ReadOnly on read operations
        """
        readonly = ReadOnly()
        readonly.run(Config(), Payload(MOCKED_GET_BODY))
        readonly.run(Config(), Payload(MOCKED_HEAD_BODY))

    def test_write_operation(self):
        """Validate ReadOnly on write operations
        """
        readonly = ReadOnly()

        with self.assertRaises(UnauthorizedException):
            readonly.run(Config(), Payload(MOCKED_POST_BODY))

        with self.assertRaises(UnauthorizedException):
            readonly.run(Config(), Payload(MOCKED_DELETE_BODY))

        with self.assertRaises(UnauthorizedException):
            readonly.run(Config(), Payload(MOCKED_PUT_BODY))
