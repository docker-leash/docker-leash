# vim:set ts=4 sw=4 et:

'''
ContainerNameTests
====
'''

import unittest

from docker_leash.checks.container_name import ContainerName
from docker_leash.exceptions import UnauthorizedException
from docker_leash.payload import Payload

payload = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create"
}

payload_foobar = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create?name=foo-bar"
}

payload_something = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create?name=hard-biture"
}


class ContainerNameTests(unittest.TestCase):
    """ Validate :class:`docker_leash.checks.ContainerName` without context
    """

    def test_empty_payload(self):
        """ Empty payload should return :exc:`UnauthorizedException`
        """
        with self.assertRaises(UnauthorizedException):
            ContainerName().run(None, Payload({}))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(".*", Payload({}))

    @staticmethod
    def test_basics():
        """ Validate wildcards cases
        """
        ContainerName().run(None, Payload(payload_something))
        ContainerName().run(None, Payload(payload_foobar))
        ContainerName().run(".*", Payload(payload_foobar))
        ContainerName().run(".*", Payload(payload_something))
        ContainerName().run("", Payload(payload_foobar))
        ContainerName().run("", Payload(payload_something))

    @staticmethod
    def test_valid_names():
        """ Valid cases
        """
        ContainerName().run("^foo-.*", Payload(payload_foobar))
        ContainerName().run(".*oo.*", Payload(payload_foobar))
        ContainerName().run("^hard-.*", Payload(payload_something))
        ContainerName().run("hard.*", Payload(payload_something))
        ContainerName().run(".*biture", Payload(payload_something))
        ContainerName().run("hard-biture", Payload(payload_something))
        ContainerName().run("hard-bitur", Payload(payload_something))

    def test_invalid_names(self):
        """ Invalid cases
        """
        with self.assertRaises(UnauthorizedException):
            ContainerName().run("^foobar.*", Payload(payload_foobar))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("^bar-foo.*", Payload(payload_foobar))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("bar-foo", Payload(payload_foobar))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("^mega-hard-biture.*", Payload(payload_something))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("ard-bitur", Payload(payload_something))
