# vim:set ts=4 sw=4 et:

import base64
import json


class Payload(object):
    """The :class:`Payload` class is responsible for decoding and storing the current analyzed request.

    :var data: The full request payload.
    :vartype data: dict or None
    :var user: The connected user.
    :vartype user: string or None
    :var method: The request HTTP method.
    :vartype method: string or None
    :var uri: The request URI.
    :vartype uri: strnig or None

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

    def __init__(self, payload=None):
        """Initialize the object.
        """
        if payload:
            self.data = self._decode_base64(payload)
            self.user = self._get_username(payload)
            self.method = self._get_method(payload)
            self.uri = self._get_uri(payload)
        print "PAYLOAD AUTHENTICATED USER: %s" % self.user
        print "PAYLOAD AUTHENTICATED URI: %s" % self.uri
        print "PAYLOAD AUTHENTICATED METHOD: %s" % self.method

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

        If the user is not connected (ie `anonymous`) the value is an empty string.

        :param dict payload: The payload to extract username.
        :return: The username.
        :rtype: string or None
        """
        if payload is None:
            return
        if "User" in payload and payload["User"]:
            return payload["User"]

    @classmethod
    def _get_method(cls, payload):
        """Extract the `Method` from the paylaod.

        :param dict payload: The payload to extract method.
        :return: The method name.
        :rtype: string or None
        """
        if payload is None:
            return
        if "RequestMethod" in payload and payload["RequestMethod"]:
            return payload["RequestMethod"]

    @classmethod
    def _get_uri(cls, payload):
        """Extract the `Uri` from the paylaod.

        :param dict payload: The payload to extract Uri.
        :return: The Uri.
        :rtype: string or None
        """
        if payload is None:
            return
        if "RequestUri" in payload and payload["RequestUri"]:
            return payload["RequestUri"]
