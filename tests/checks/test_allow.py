# vim:set ts=4 sw=4 et:

import unittest

from app.checks.allow import Allow
from app.config import Config


class CheckAllowTests(unittest.TestCase):

    def test_init(self):
        allow = Allow()
        allow.run(Config(), {})
