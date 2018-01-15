# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.allow import Allow
from docker_leash.config import Config


class CheckAllowTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        allow = Allow()
        allow.run(Config(), {})
