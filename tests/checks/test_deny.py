# vim:set ts=4 sw=4 et:
'''
CheckDenyTests
--------------
'''

import unittest

from docker_leash.checks.deny import Deny
from docker_leash.config import Config
from docker_leash.exceptions import UnauthorizedException


class CheckDenyTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.Deny`
    """

    def test_init(self):
        """Validate Deny initialization
        """
        deny = Deny()
        with self.assertRaises(UnauthorizedException):
            deny.run(Config(), {})
