# vim:set ts=4 sw=4 et:
'''
UserTests
---------
'''

import unittest

from docker_leash.checks.user import User
from docker_leash.exceptions import (ConfigurationException,
                                     InvalidRequestException,
                                     UnauthorizedException)
from docker_leash.payload import Payload

PAYLOAD_UNDEFINED = {
    "User": "foobar",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {},
}
PAYLOAD_EMPTY = {
    "User": "foobar",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "User": "",
    },
}

PAYLOAD_FOOBAR = {
    "User": "foobar",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "User": "foobar",
    },
}

PAYLOAD_FOO = {
    "User": "foo",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "User": "foobar",
    },
}

PAYLOAD_SOMEONE = {
    "User": "foobar",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "User": "someone",
    },
}


class UserTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.User`
    """

    def test_empty_payload(self):
        """Empty payload should return :exc:`InvalidRequestException`
        """
        with self.assertRaises(InvalidRequestException):
            User().run(None, Payload({}))

        with self.assertRaises(InvalidRequestException):
            User().run(".*", Payload({}))

        with self.assertRaises(InvalidRequestException):
            User().run([".*"], Payload({}))

    def test_invalid_configuration(self):
        """Incomplete module configuration :exc:`ConfigurationException`
        """
        with self.assertRaises(ConfigurationException):
            User().run(None, Payload(PAYLOAD_EMPTY))

    def test_empty_user(self):
        """Empty user is allowed and always accepted
        """
        User().run(".*", Payload(PAYLOAD_EMPTY))
        User().run(".+", Payload(PAYLOAD_EMPTY))

        User().run([".*"], Payload(PAYLOAD_EMPTY))
        User().run([".+"], Payload(PAYLOAD_EMPTY))

        User().run([".*", ".+"], Payload(PAYLOAD_EMPTY))

    def test_undefined_user(self):
        """Undefined user is allowed and always accepted
        """
        User().run(".*", Payload(PAYLOAD_UNDEFINED))
        User().run(".+", Payload(PAYLOAD_UNDEFINED))

        User().run([".*"], Payload(PAYLOAD_UNDEFINED))
        User().run([".+"], Payload(PAYLOAD_UNDEFINED))

        User().run([".*", ".+"], Payload(PAYLOAD_UNDEFINED))

    def test_user_regex(self):
        """Validate user regex matching
        """

        User().run(".+", Payload(PAYLOAD_FOOBAR))
        User().run(".*", Payload(PAYLOAD_FOOBAR))
        User().run("foobar", Payload(PAYLOAD_FOOBAR))
        User().run("^foo.*$", Payload(PAYLOAD_FOOBAR))
        User().run("^foobar$", Payload(PAYLOAD_FOOBAR))
        User().run(".*bar$", Payload(PAYLOAD_FOOBAR))
        User().run(".*foobar.*", Payload(PAYLOAD_FOOBAR))

        User().run(".+", Payload(PAYLOAD_FOO))
        User().run(".*", Payload(PAYLOAD_FOO))
        User().run("^foo.*$", Payload(PAYLOAD_FOO))

        with self.assertRaises(UnauthorizedException):
            User().run("someone", Payload(PAYLOAD_FOOBAR))
            User().run("^foobar2$", Payload(PAYLOAD_FOOBAR))
            User().run("^foobar.+$", Payload(PAYLOAD_FOOBAR))
            User().run("^.+foobar$", Payload(PAYLOAD_FOOBAR))
            User().run("^.+foobar.+$", Payload(PAYLOAD_FOOBAR))
            User().run("foobar", Payload(PAYLOAD_FOO))
            User().run("^foobar$", Payload(PAYLOAD_FOO))
            User().run(".*bar$", Payload(PAYLOAD_FOO))
            User().run(".*foobar.*", Payload(PAYLOAD_FOO))
            User().run("someone", Payload(PAYLOAD_FOO))
            User().run("^foobar2$", Payload(PAYLOAD_FOO))
            User().run("^foobar.+$", Payload(PAYLOAD_FOO))
            User().run("^.+foobar$", Payload(PAYLOAD_FOO))
            User().run("^.+foobar.+$", Payload(PAYLOAD_FOO))

    def test_connected_user(self):
        """Force user to be connected user
        """
        User().run("^$USER$", Payload(PAYLOAD_FOOBAR))
        User().run("$USER", Payload(PAYLOAD_FOOBAR))

        User().run("$USER", Payload(PAYLOAD_FOO))
        with self.assertRaises(UnauthorizedException):
            User().run("^$USER$", Payload(PAYLOAD_FOO))

    def test_user_name_can_be_a_list(self):
        """names could be presented as a list

        In such case, entries are compared with a 'or'.
        """
        User().run(["^USER$", "^foobar$"], Payload(PAYLOAD_FOOBAR))
        User().run(["^USER$", "^foobar$"], Payload(PAYLOAD_FOO))

        User().run(["^foo$", "^foobar$"], Payload(PAYLOAD_FOOBAR))
        User().run(["^foo$", "^foobar$"], Payload(PAYLOAD_FOO))

        with self.assertRaises(UnauthorizedException):
            User().run(["^foo$", "^foobar$"], Payload(PAYLOAD_SOMEONE))
            User().run(["^USER$", "^foobar$"], Payload(PAYLOAD_SOMEONE))
