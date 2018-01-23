# vim:set ts=4 sw=4 et:
'''
Payload
=======
'''

import base64
import json

from docker_leash.exceptions import InvalidRequestException

from . import app


class Payload(object):
    """The :class:`Payload` class is responsible for decoding and storing
    the current analyzed request.

    :var data: The full request payload.
    :vartype data: dict or None
    :var user: The connected user.
    :vartype user: str or None
    :var method: The request HTTP method.
    :vartype method: str or None
    :var uri: The request URI.
    :vartype uri: str or None
    :var headers: The request Headers.
    :vartype headers: dict or None

    :param payload: The paylaod to analyze and store.
    :type payload: dict or None
    """

    # Immutable properties
    #: The full request payload
    data = None

    #: The connected user
    user = None

    #: The request HTTP method
    method = None

    #: The request URI
    uri = None

    #: The request Headers
    headers = None

    def __init__(self, payload=None):
        """Initialize the object.
        """
        if not payload:
            raise InvalidRequestException("Payload is empty")

        self.headers = self._get_headers(payload)
        self.data = self._decode_base64(payload)
        self.user = self._get_username(payload)
        self.method = self._get_method(payload)
        self.uri = self._get_uri(payload)
        app.logger.info(
            "PAYLOAD AUTHENTICATED USER=%r URI=%r METHOD=%r",
            self.user,
            self.uri,
            self.method,
        )

    def get_host(self):
        """Get the hostname
        """
        if self.headers and "Host" in self.headers:
            return self.headers["Host"]

    @classmethod
    def _decode_base64(cls, payload):
        """Decode some parts of the payload from base64 to dict.

        :param dict payload: The payload to fully base64 decode.
        :return: The fully decoded payload.
        :rtype: dict
        """
        data = payload.copy()
        if "RequestBody" in data:
            if isinstance(data["RequestBody"], dict):
                return data

            data["RequestBody"] = json.loads(
                base64.b64decode(data["RequestBody"])
            )
        return data

    @classmethod
    def _get_username(cls, payload):
        """Extract the `User` from the paylaod.

        If the user is not connected (i.e.: `anonymous`), the value is an empty string.

        :param dict payload: The payload to extract username.
        :return: The username.
        :rtype: str or None
        """
        if payload and "User" in payload and payload["User"]:
            return payload["User"]

        return None

    @classmethod
    def _get_method(cls, payload):
        """Extract the `Method` from the paylaod.

        :param dict payload: The payload to extract method.
        :return: The method name.
        :rtype: str or None
        """
        if payload and "RequestMethod" in payload and payload["RequestMethod"]:
            return payload["RequestMethod"]

        raise InvalidRequestException("Payload is missing RequestMethod")

    @classmethod
    def _get_uri(cls, payload):
        """Extract the `URI` from the paylaod.

        :param dict payload: The payload to extract URI.
        :return: The URI.
        :rtype: str or None
        """
        if payload and "RequestUri" in payload and payload["RequestUri"]:
            return payload["RequestUri"]

        return None

    @classmethod
    def _get_headers(cls, payload):
        """Extract the `Headers` from the paylaod.

        :param dict payload: The payload to extract URI.
        :return: The Headers.
        :rtype: dict or None
        """
        if payload and "RequestHeaders" in payload and payload["RequestHeaders"]:
            return payload["RequestHeaders"]

        raise InvalidRequestException("Headers missing from payload")
