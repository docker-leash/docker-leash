# vim:set ts=4 sw=4 et:
'''
BaseTests
===========
'''

import unittest

from docker_leash import app


class BaseTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.BaseTests`
    """

    def test_debug_logging(self):
        """Activate logging
        """
        with app.app_context():
            app.config["DEBUG"] = True
