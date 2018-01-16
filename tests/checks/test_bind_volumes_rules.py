# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.bind_volumes import Rules


class BindVolumesRulesTests(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(TypeError):
            Rules(None)

        with self.assertRaises(TypeError):
            Rules("-/.*")

        with self.assertRaises(TypeError):
            Rules("")

        self.assertIsInstance(Rules([]), Rules)

    def test_rules_to_str(self):
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
        args = [
            r'-',
            r'-[]^] [',
            r'-/[^foo',
        ]
        rules = Rules(args)
        self.assertEqual(str(rules), "Rules([])".format())
