# vim:set ts=4 sw=4 et:
'''
CheckAllowTests
---------------
'''

import unittest

from docker_leash.checks.allow import Allow
from docker_leash.config import Config


class CheckAllowTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.Allow`
    """

    @classmethod
    def test_init(cls):
        """Validate Allow initialization
        """
        allow = Allow()
        allow.run(Config(), {})
