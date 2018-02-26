# vim:set ts=4 sw=4 et:
'''
ContainerNameTestsFunctionnal
-----------------------------
'''

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ContainerNameTestsFunctionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of :cls:`docker_leash.checks.ContainerName`
    """

    def test_create_authenticated_valid(self):
        """A valid container create request as authenticated user
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "User": "jre",
            "UserAuthNMethod": "TLS",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_create_authenticated_invalid(self):
        """An invalid container create request as authenticated user
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foobar",
            "User": "jre",
            "UserAuthNMethod": "TLS",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_valid(self):
        """A valid container create request as anonymous user
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_unauthenticated_invalid(self):
        """An invalid container create request as anonymous user
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create?name=foo-bar",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_authenticated_without_static_name(self):
        """No container name specified as authenticated
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "jre",
            "UserAuthNMethod": "TLS",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_create_anonymous_without_static_name(self):
        """No container name specified as anonynous
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
