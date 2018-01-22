# vim:set ts=4 sw=4 et:
'''
ContainerNameTests
------------------
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

payload_user = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create?name=someone-love-me"
}

payload_username = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create?name=someoneNAME-love-me"
}


class ContainerNameTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.ContainerName`
    """

    def test_empty_payload(self):
        """Empty payload should return :exc:`InvalidRequestException`
        """
        with self.assertRaises(UnauthorizedException):
            ContainerName().run(None, Payload({}))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(".*", Payload({}))

    @staticmethod
    def test_basics():
        """Validate wildcards cases
        """
        ContainerName().run(None, Payload(payload_something))
        ContainerName().run(None, Payload(payload_foobar))
        ContainerName().run(".*", Payload(payload_foobar))
        ContainerName().run(".*", Payload(payload_something))
        ContainerName().run("", Payload(payload_foobar))
        ContainerName().run("", Payload(payload_something))

    @staticmethod
    def test_valid_names():
        """Valid cases
        """
        ContainerName().run("^foo-.*", Payload(payload_foobar))
        ContainerName().run(".*oo.*", Payload(payload_foobar))
        ContainerName().run("^hard-.*", Payload(payload_something))
        ContainerName().run("hard.*", Payload(payload_something))
        ContainerName().run(".*biture", Payload(payload_something))
        ContainerName().run("hard-biture", Payload(payload_something))
        ContainerName().run("hard-bitur", Payload(payload_something))

    def test_name_can_be_a_list(self):
        """names could be presented as a list

        In such case, entries are compared with a 'or'.
        """
        ContainerName().run(["^foo-.*", "^$USER-.*"], Payload(payload_foobar))
        ContainerName().run(["^foo-.*", "^$USER-.*"], Payload(payload_user))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(["^foo-.*", "^\$USER-.*"], Payload(payload_user))

    def test_invalid_names(self):
        """Invalid cases
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

    def test_username_in_image_name(self):
        """Replace $USER by connected username
        """
        ContainerName().run("^$USER-.*", Payload(payload_user))
        ContainerName().run("^$USERNAME-.*", Payload(payload_username))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("^$USER-.*", Payload(payload_something))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(r"^\$USER-.*", Payload(payload_user))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(r"^\$USER-.*", Payload(payload_something))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run("^$USER-.*", Payload(payload_username))

        with self.assertRaises(UnauthorizedException):
            ContainerName().run(r"^\$USER-.*", Payload(payload_username))
