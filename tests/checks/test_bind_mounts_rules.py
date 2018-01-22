# vim:set ts=4 sw=4 et:
'''
BindMountsRulesTests
---------------------
'''

import unittest

from docker_leash.checks.bind_mounts import Rules


class BindMountsRulesTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.BindMountsRules`
    """

    def test_init(self):
        """Check Rules parameter type
        """
        with self.assertRaises(TypeError):
            Rules(None)

        with self.assertRaises(TypeError):
            Rules("-/.*")

        with self.assertRaises(TypeError):
            Rules("")

        self.assertIsInstance(Rules([]), Rules)

    def test_rules_to_str(self):
        """Validate rules convertion to str
        """
        args = [
            r'-/.*',
            r'+/foo/',
            r'-/proc/[0-9]*',
            r'-/proc/[^a-z]*',
            r'-.*/\..+',
        ]
        rules = Rules(args)
        self.assertEqual(str(rules), "Rules({!r})".format(args))

    def test_invalid_rules_to_str(self):
        """Validate wrong rules convertion to str
        """
        args = [
            r'-',
            r'-[]^] [',
            r'-/[^foo',
        ]
        rules = Rules(args)
        self.assertEqual(str(rules), "Rules([])".format())
