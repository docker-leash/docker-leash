# vim:set ts=4 sw=4 et:

'''
BaseCheckTests
----
'''

import unittest

from docker_leash.checks.base import BaseCheck
from docker_leash.config import Config
from docker_leash.payload import Payload


class BaseCheckTests(unittest.TestCase):
    """Validate :class:`docker_leash.checks.BaseCheck` features
    """

    def test_init(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.run` raise
        :exc:`NotImplementedError`
        """
        base = BaseCheck()
        with self.assertRaises(NotImplementedError):
            base.run(Config(), {})

    def test_replace_user_string(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.replace_user` can
        replace user on `string`
        """
        base = BaseCheck()

        payload = Payload({"User": "mal"})
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertEqual(result, "mal-loves-me")

        result = BaseCheck.replace_user("$USERNAME-loves-me", payload)
        self.assertEqual(result, "malNAME-loves-me")

        result = BaseCheck.replace_user("do-you-think-$USER-loves-me", payload)
        self.assertEqual(result, "do-you-think-mal-loves-me")

        result = BaseCheck.replace_user("$USER-is-$USER", payload)
        self.assertEqual(result, "mal-is-mal")

        payload = Payload({"User": "rda"})
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertEqual(result, "rda-loves-me")

    def test_replace_user_list(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.replace_user` can
        replace user on `list`
        """
        base = BaseCheck()
        values = [
            "$USER-loves-me",
            "$USERNAME-loves-me",
            "do-you-think-$USER-loves-me",
            "of-course"
        ]
        attended = [
            "mal-loves-me",
            "malNAME-loves-me",
            "do-you-think-mal-loves-me",
            "of-course"
        ]

        payload = Payload({"User": "mal"})
        result = BaseCheck.replace_user(values, payload)
        self.assertListEqual(result, attended)

    def test_replace_user_as_anonymous(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.replace_user` returns
        `None` when connected as anonymous
        """
        base = BaseCheck()

        payload = Payload({"User": None})
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertIsNone(result)

        payload = Payload({})
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertIsNone(result)

    def test_replace_user_with_escape(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.replace_user` don't
        replace when '$' is escaped
        """
        base = BaseCheck()

        payload = Payload({"User": "mal"})
        result = BaseCheck.replace_user(r"\$USER-loves-me", payload)
        self.assertEqual(result, r"\$USER-loves-me")

        result = BaseCheck.replace_user([r"\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\$USER-loves-me"])

        result = BaseCheck.replace_user([r"\\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\mal-loves-me"])

        result = BaseCheck.replace_user([r"\\\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\$USER-loves-me"])

        payload = Payload({"User": None})
        result = BaseCheck.replace_user(r"\$USER-loves-me", payload)
        self.assertEqual(result, r"\$USER-loves-me")

        result = BaseCheck.replace_user([r"\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\$USER-loves-me"])
