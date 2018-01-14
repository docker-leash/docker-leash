# vim:set ts=4 sw=4 et:

import unittest

from app.checks.allow import Allow
from app.config import Config


class CheckAllowTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        allow = Allow()
        allow.run(Config(), {})
