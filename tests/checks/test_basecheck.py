# vim:set ts=4 sw=4 et:

import unittest

from app.checks.base import BaseCheck
from app.config import Config


class BaseCheckTests(unittest.TestCase):

    def test_init(self):
        base = BaseCheck()
        with self.assertRaises(NotImplementedError):
            base.run(Config(), {})
