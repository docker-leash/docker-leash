# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.base import BaseCheck
from docker_leash.config import Config


class BaseCheckTests(unittest.TestCase):

    def test_init(self):
        base = BaseCheck()
        with self.assertRaises(NotImplementedError):
            base.run(Config(), {})
