# vim:set ts=4 sw=4 et:

import unittest

from app.checks.deny import Deny
from app.config import Config
from app.exceptions import UnauthorizedException


class CheckDenyTests(unittest.TestCase):

    def test_init(self):
        deny = Deny()
        with self.assertRaises(UnauthorizedException):
            deny.run(Config(), {})
