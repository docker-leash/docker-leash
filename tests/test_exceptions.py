# vim:set ts=4 sw=4 et:

import unittest

from app.exceptions import NotForMeException, UnauthorizedException


class ExceptionsTests(unittest.TestCase):

    def test_not_for_me_exception(self):
        self.assertRaises(NotForMeException())

    def test_unauthorized_exception(self):
        self.assertRaises(UnauthorizedException("Some error"))

    def test_unauthorized_exception_string(self):
        msg = "Some error"
        try:
            raise UnauthorizedException(msg)
        except UnauthorizedException as e:
            self.assertEqual(msg, str(e))

    def test_unauthorized_exception_json(self):
        msg = "Some error"
        try:
            raise UnauthorizedException(msg)
        except UnauthorizedException as e:
            response = {
                "Allow": False,
                "Msg": msg
            }
            self.assertEqual(response, e.json())
