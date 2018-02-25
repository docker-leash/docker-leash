# vim:set ts=4 sw=4 et:
'''
PayloadTests
============
'''

import unittest

from docker_leash.exceptions import InvalidRequestException
from docker_leash.payload import Payload

MOCKED_MISSING_HEADERS = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
}

MOCKED_MISSING_HOST = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {},
}

MOCKED_BODY = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {},
    "Host": "other01",
}

MOCKED_BODY_2 = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.32/containers/json",
    "RequestHeaders": {},
    "Host": "other01",
}

MOCKED_BODY_ANONYMOUS_1 = {
    "User": "",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {},
    "Host": "other01",
}

MOCKED_BODY_ANONYMOUS_2 = {
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
    "RequestHeaders": {},
    "Host": "other01",
}


class PayloadTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.Payload`
    """

    def test_payload_need_headers(self):
        """Payload minimal check
        """
        with self.assertRaises(InvalidRequestException):
            Payload()

        with self.assertRaises(InvalidRequestException):
            Payload(payload=MOCKED_MISSING_HEADERS)

    def test_get_host(self):
        """Get host from headers
        """
        payload = Payload(payload=MOCKED_MISSING_HOST)
        self.assertEqual(payload.get_host(), '')

        payload = Payload(payload=MOCKED_BODY)
        self.assertEqual(payload.get_host(), 'other01')

    def test_payload_is_not_shared(self):
        """Payload object are Immutable
        """
        payload1 = Payload(MOCKED_BODY)
        self.assertNotEqual(payload1.data, None)
        self.assertNotEqual(payload1.user, None)

        payload2 = Payload(MOCKED_BODY_2)
        self.assertNotEqual(payload2.data, None)
        self.assertNotEqual(payload2.user, None)

        # Now config should be the same on first object
        self.assertNotEqual(payload1.data, payload2.data)

    def test_decode_RequestBody(self):
        """Decode request body
        """
        payload = Payload(payload=MOCKED_BODY)
        decoded = payload._decode_base64(MOCKED_BODY)

        attended_response = {'foo': 'bar'}

        self.assertEqual(attended_response, decoded["RequestBody"])

    def test_receive_already_decoded_base64(self):
        """Already decoded request body
        """
        body = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": "eyJmb28iOiAiYmFyIn0=",  # '{"foo": "bar"}'
            "RequestHeaders": {
                "Host": "other01"
            },
        }
        body_decoded = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {"foo": "bar"},
            "RequestHeaders": {
                "Host": "other01"
            },
        }

        payload = Payload(payload=body)
        attended_response = {'foo': 'bar'}
        self.assertEqual(attended_response, payload.data["RequestBody"])

        payload = Payload(payload=body_decoded)
        attended_response = {'foo': 'bar'}
        self.assertEqual(attended_response, payload.data["RequestBody"])

    def test_get_username(self):
        """Retrieve username
        """
        payload = Payload(payload=MOCKED_BODY)

        username = payload._get_username(MOCKED_BODY)
        self.assertEqual(username, "someone")

        username = payload._get_username(MOCKED_BODY_ANONYMOUS_1)
        self.assertEqual(username, None)

        username = payload._get_username(MOCKED_BODY_ANONYMOUS_2)
        self.assertEqual(username, None)

        username = payload._get_username(None)
        self.assertEqual(username, None)

    def test_get_method(self):
        """Retrieve method
        """
        payload = Payload(payload=MOCKED_BODY)

        method = payload._get_method(MOCKED_BODY)
        self.assertEqual(method, MOCKED_BODY['RequestMethod'])

        with self.assertRaises(InvalidRequestException):
            method = payload._get_method(None)

    def test_get_uri(self):
        """Retrieve uri
        """
        payload = Payload(payload=MOCKED_BODY)

        uri = payload._get_uri(MOCKED_BODY)
        self.assertEqual(uri, MOCKED_BODY['RequestUri'])

        uri = payload._get_uri(None)
        self.assertEqual(uri, None)

    def test_run_store_values(self):
        """Check if payload values are really stored
        """
        with self.assertRaises(InvalidRequestException):
            payload = Payload(payload=None)

        payload = Payload(payload=MOCKED_BODY)
        self.assertNotEqual(payload.data, None)
        self.assertEqual(payload.user, MOCKED_BODY['User'])
        self.assertEqual(payload.method, MOCKED_BODY['RequestMethod'])
        self.assertEqual(payload.uri, MOCKED_BODY['RequestUri'])
