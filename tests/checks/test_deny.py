# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.deny import Deny
from docker_leash.config import Config
from docker_leash.exceptions import UnauthorizedException


class CheckDenyTests(unittest.TestCase):

    def test_init(self):
        deny = Deny()
        with self.assertRaises(UnauthorizedException):
            deny.run(Config(), {})
