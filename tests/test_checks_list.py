# vim:set ts=4 sw=4 et:
'''
ChecksTests
===========
'''

import unittest

from docker_leash.checks_list import Checks


class ChecksTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.Checks`
    """

    @classmethod
    def test_init(cls):
        """Validate Checks creation without error
        """
        Checks()

    def test_contains(self):
        """Check __contains__ function
        """
        item = {'Allow': None}
        checks = Checks()
        checks.add(item)
        self.assertTrue(item in checks)

    def test_repr(self):
        """Check __repr__ function
        """
        checks = Checks()
        checks.add({'Allow': None})
        self.assertEqual(checks.__repr__(), "[{'args': None, 'name': 'Allow'}]")

    def test_equal(self):
        """Check __equal__ function
        """
        checks = Checks()
        checks.add({'Allow': None})
        self.assertEqual(checks, [{'args': None, 'name': 'Allow'}])

    def test_equal_unordered(self):
        """Check __equal__ function unordered
        """
        checks = Checks()
        checks.add({'Deny': None})
        checks.add({'Allow': None})
        self.assertEqual(checks, [
            {'args': None, 'name': 'Allow'},
            {'args': None, 'name': 'Deny'},
        ])

    def test_structure_convert(self):
        """Check _structure_convert function
        """
        checks = Checks()
        result = checks._structure_convert({'Allow': None})
        self.assertEqual(result, {'args': None, 'name': 'Allow'})

    def test_add_two_elements(self):
        """Add two elements
        """
        checks = Checks()
        checks.add({'Allow': None})
        checks.add({'pathCheck': ['-/', '+/home/$USER', '+/0']})
        self.assertEqual(len(checks), 2)
        self.assertEqual(checks[0], {'args': None, 'name': 'Allow'})
        self.assertEqual(
            checks[1], {'args': ['-/', '+/home/$USER', '+/0'], 'name': 'pathCheck'})

    def test_add_two_same_elements(self):
        """Add the same element two times
        """
        checks = Checks()
        checks.add({'Allow': None})
        checks.add({'Allow': None})
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0], {'args': None, 'name': 'Allow'})

    def test_overlapped_elements(self):
        """Add elements having different arguments
        """
        checks = Checks()
        checks.add({"pathCheck": ["-/", "+/home/$USER", "+/0"]})
        checks.add({"Allow": None})
        checks.add({"containerNameCheck": {"startwith": ['foo', 'bar']}})
        checks.add({"pathCheck": ["+/mnt/usbkey"]})
        checks.add({"Allow": None})
        self.assertEqual(len(checks), 4)
