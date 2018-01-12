# vim:set ts=4 sw=4 et:

import base64
import json


class Payload():

    # Immutable properties
    data = None
    user = None
    method = None
    uri = None

    def __init__(self, payload=None):
        if payload:
            self.data = self._decode_base64(payload)
            self.user = self._get_username(payload)
            self.method = self._get_method(payload)
            self.uri = self._get_uri(payload)
        print "PAYLOAD AUTHENTICATED USER: %s" % self.user
        print "PAYLOAD AUTHENTICATED URI: %s" % self.uri
        print "PAYLOAD AUTHENTICATED METHOD: %s" % self.method

    def _decode_base64(self, payload):
        # We know some part are base64 encoded, decode them here
        data = payload.copy()
        if "RequestBody" in data:
            data["RequestBody"] = json.loads(
                base64.b64decode(data["RequestBody"])
            )
        return data

    def _get_username(self, payload):
        if payload is None:
            return
        if "User" in payload and payload["User"]:
            return payload["User"]

    def _get_method(self, payload):
        if payload is None:
            return
        if "RequestMethod" in payload and payload["RequestMethod"]:
            return payload["RequestMethod"]

    def _get_uri(self, payload):
        if payload is None:
            return
        if "RequestUri" in payload and payload["RequestUri"]:
            return payload["RequestUri"]
