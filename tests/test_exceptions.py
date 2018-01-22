# vim:set ts=4 sw=4 et:
'''
DockerLeashExceptionTests
=========================
'''

import unittest

from docker_leash.exceptions import (DockerLeashException,
                                     NoSuchCheckModuleException,
                                     UnauthorizedException)


class DockerLeashExceptionTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.DockerLeashException`
    """

    def test_docker_leash_base_exception(self):
        """Force raise exception
        """
        self.assertRaises(DockerLeashException("Some error"))

    def test_docker_leash_base_exception_string(self):
        """Message is accessible
        """
        msg = "Some error"
        try:
            raise DockerLeashException(msg)
        except DockerLeashException as e:
            self.assertEqual(msg, str(e))

    def test_docker_leash_base_exception_json(self):
        """Exception as json
        """
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
    """Validation of :cls:`docker_leash.UnauthorizedException`
    """

    def test_unauthorized_exception(self):
        """Raise :exc:`UnauthorizedException` with different parameters
        """
        self.assertRaises(UnauthorizedException())
        self.assertRaises(UnauthorizedException(None))
        self.assertRaises(UnauthorizedException(""))
        self.assertRaises(UnauthorizedException("Some error"))


class NoSuchCheckModuleExceptionTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.NoSuchCheckModuleException`
    """

    def test_no_such_check_module_exception(self):
        """Raise :exc:`NoSuchCheckModuleException` with different parameters
        """
        self.assertRaises(NoSuchCheckModuleException())
        self.assertRaises(NoSuchCheckModuleException(None))
        self.assertRaises(NoSuchCheckModuleException(""))
        self.assertRaises(NoSuchCheckModuleException("Some error"))
