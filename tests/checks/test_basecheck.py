# vim:set ts=4 sw=4 et:
'''
BaseCheckTests
--------------
'''

import unittest

from docker_leash.checks.base import BaseCheck
from docker_leash.config import Config
from docker_leash.payload import Payload


class BaseCheckTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.BindVolumesRules`
    """

    def test_init(self):
        """Check that :meth:`docker_leash.checks.BaseCheck.run` raise
        :exc:`NotImplementedError`
        """
        base = BaseCheck()
        with self.assertRaises(NotImplementedError):
            base.run(Config(), {})

    def test_replace_user_string(self):
        """Check that `replace_user` can eplace user on str
        """
        base = BaseCheck()

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertEqual(result, "mal-loves-me")

        result = BaseCheck.replace_user("$USERNAME-loves-me", payload)
        self.assertEqual(result, "malNAME-loves-me")

        result = BaseCheck.replace_user("do-you-think-$USER-loves-me", payload)
        self.assertEqual(result, "do-you-think-mal-loves-me")

        result = BaseCheck.replace_user("$USER-is-$USER", payload)
        self.assertEqual(result, "mal-is-mal")

        payload = Payload({
            "User": "rda",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertEqual(result, "rda-loves-me")

    def test_replace_user_list(self):
        """Check that `replace_user` can replace user on `list`
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

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user(values, payload)
        self.assertListEqual(result, attended)

    def test_replace_user_as_anonymous(self):
        """Check that `replace_user` remove items containing $USER: str
        """
        base = BaseCheck()

        payload = Payload({
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertIsNone(result)

        payload = Payload({
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user("$USER-loves-me", payload)
        self.assertIsNone(result)

        replace when '$' is escaped
    def test_user_replace_user_with_escape_list(self):
        """Check that `replace_user` don't replace when '$' is escaped: str
        """
        base = BaseCheck()

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user(r"\$USER-loves-me", payload)
        self.assertEqual(result, r"\$USER-loves-me")

        result = BaseCheck.replace_user([r"\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\$USER-loves-me"])

        result = BaseCheck.replace_user([r"\\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\\mal-loves-me"])

        result = BaseCheck.replace_user([r"\\\$USER-loves-me"], payload)
        self.assertEqual(result, [r"\\\$USER-loves-me"])

        payload = Payload({
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestHeaders": {
                "Host": "other01"
            }
        })
        result = BaseCheck.replace_user(r"\$USER-loves-me", payload)
        self.assertIsNone(result)

        result = BaseCheck.replace_user([r"\$USER-loves-me"], payload)
        self.assertEqual(result, [])
