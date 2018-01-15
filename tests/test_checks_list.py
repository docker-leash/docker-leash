# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks_list import Checks


class ChecksTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        Checks()

    def test_contains(self):
        item = {'Allow': None}
        checks = Checks()
        checks.add(item)
        self.assertTrue(item in checks)

    def test_repr(self):
        checks = Checks()
        checks.add({'Allow': None})
        self.assertEqual(checks.__repr__(), "[{'args': None, 'name': 'Allow'}]")

    def test_equal(self):
        checks = Checks()
        checks.add({'Allow': None})
        self.assertEqual(checks, [{'args': None, 'name': 'Allow'}])

    def test_equal_unordered(self):
        checks = Checks()
        checks.add({'Deny': None})
        checks.add({'Allow': None})
        self.assertEqual(checks, [
            {'args': None, 'name': 'Allow'},
            {'args': None, 'name': 'Deny'},
        ])

    def test_structure_convert(self):
        checks = Checks()
        result = checks._structure_convert({'Allow': None})
        self.assertEqual(result, {'args': None, 'name': 'Allow'})

    def test_add_two_elements(self):
        checks = Checks()
        checks.add({'Allow': None})
        checks.add({'pathCheck': ['-/', '+/home/$USER', '+/0']})
        self.assertEqual(len(checks), 2)
        self.assertEqual(checks[0], {'args': None, 'name': 'Allow'})
        self.assertEqual(
            checks[1], {'args': ['-/', '+/home/$USER', '+/0'], 'name': 'pathCheck'})

    def test_add_two_same_elements(self):
        checks = Checks()
        checks.add({'Allow': None})
        checks.add({'Allow': None})
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0], {'args': None, 'name': 'Allow'})

    def test_overlapped_elements(self):
        checks = Checks()
        checks.add({"pathCheck": ["-/", "+/home/$USER", "+/0"]})
        checks.add({"Allow": None})
        checks.add({"containerNameCheck": {"startwith": ['foo', 'bar']}})
        checks.add({"pathCheck": ["+/mnt/usbkey"]})
        checks.add({"Allow": None})
        self.assertEqual(len(checks), 4)
