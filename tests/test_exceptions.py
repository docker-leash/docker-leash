# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.exceptions import (DockerLeashException,
                                     NoSuchCheckModuleException,
                                     UnauthorizedException)


class DockerLeashExceptionTests(unittest.TestCase):

    def test_docker_leash_base_exception(self):
        self.assertRaises(DockerLeashException("Some error"))

    def test_docker_leash_base_exception_string(self):
        msg = "Some error"
        try:
            raise DockerLeashException(msg)
        except DockerLeashException as e:
            self.assertEqual(msg, str(e))

    def test_docker_leash_base_exception_json(self):
        msg = "Some error"
        try:
            raise DockerLeashException(msg)
        except DockerLeashException as e:
            response = {
                "Allow": False,
                "Msg": msg
            }
            self.assertEqual(response, e.json())


class UnauthorizedExceptionTests(unittest.TestCase):

    def test_unauthorized_exception(self):
        self.assertRaises(UnauthorizedException())
        self.assertRaises(UnauthorizedException(None))
        self.assertRaises(UnauthorizedException(""))
        self.assertRaises(UnauthorizedException("Some error"))


class NoSuchCheckModuleExceptionTests(unittest.TestCase):

    def test_no_such_check_module_exception(self):
        self.assertRaises(NoSuchCheckModuleException())
        self.assertRaises(NoSuchCheckModuleException(None))
        self.assertRaises(NoSuchCheckModuleException(""))
        self.assertRaises(NoSuchCheckModuleException("Some error"))
