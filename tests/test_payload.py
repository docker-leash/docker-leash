# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.payload import Payload

mocked_body = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
}

mocked_body_anonymous_1 = {
    "User": "",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
}

mocked_body_anonymous_2 = {
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
}

class payloadTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        Payload()

    def test_payload_is_not_shared(self):
        payload1 = Payload()
        self.assertEqual(payload1.data, None)
        self.assertEqual(payload1.user, None)

        payload2 = Payload(mocked_body)
        self.assertNotEqual(payload2.data, None)
        self.assertNotEqual(payload2.user, None)

        # Now config should be the same on first object
        self.assertNotEqual(payload1.data, payload2.data)

    # def test_decode_empty_body(self):
    #     payload = Payload()
    #     decoded = payload._decode_base64(mocked_body)
    #
    #     attended_response = {'foo': 'bar'}
    #
    #     self.assertEqual(attended_response, decoded["RequestBody"])

    def test_decode_RequestBody(self):
        payload = Payload()
        decoded = payload._decode_base64(mocked_body)

        attended_response = {'foo': 'bar'}

        self.assertEqual(attended_response, decoded["RequestBody"])

    def test_receive_already_decoded_base64(self):
        body = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
        }
        body_decoded = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "RequestBody": {"foo": "bar"}
        }

        payload = Payload(payload=body)
        attended_response = {'foo': 'bar'}
        self.assertEqual(attended_response, payload.data["RequestBody"])

        payload = Payload(payload=body_decoded)
        attended_response = {'foo': 'bar'}
        self.assertEqual(attended_response, payload.data["RequestBody"])

    def test_get_username(self):
        payload = Payload()

        username = payload._get_username(mocked_body)
        self.assertEqual(username, "someone")

        username = payload._get_username(mocked_body_anonymous_1)
        self.assertEqual(username, None)

        username = payload._get_username(mocked_body_anonymous_2)
        self.assertEqual(username, None)

        username = payload._get_username(None)
        self.assertEqual(username, None)

    def test_get_method(self):
        payload = Payload()

        method = payload._get_method(mocked_body)
        self.assertEqual(method, mocked_body['RequestMethod'])

        method = payload._get_method(None)
        self.assertEqual(method, None)

    def test_get_uri(self):
        payload = Payload()

        uri = payload._get_uri(mocked_body)
        self.assertEqual(uri, mocked_body['RequestUri'])

        uri = payload._get_uri(None)
        self.assertEqual(uri, None)

    def test_run_store_values(self):
        payload = Payload(payload=None)
        self.assertEqual(payload.data, None)
        self.assertEqual(payload.user, None)
        self.assertEqual(payload.method, None)
        self.assertEqual(payload.uri, None)

        payload = Payload(payload=mocked_body)
        self.assertNotEqual(payload.data, None)
        self.assertEqual(payload.user, mocked_body['User'])
        self.assertEqual(payload.method, mocked_body['RequestMethod'])
        self.assertEqual(payload.uri, mocked_body['RequestUri'])
