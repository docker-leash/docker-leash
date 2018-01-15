# vim:set ts=4 sw=4 et:

import unittest

from docker_leash.checks.bind_volumes import BindVolumes, Rules
from docker_leash.exceptions import UnauthorizedException

payload_minimal = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": []
        }
    }
}

payload_foo = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": {
        "HostConfig": {
            "Binds": [
                '/foo',
                '/foo/bar',
                '/foo/bar/team',
            ]
        }
    }
}

class BindVolumesRulesTests(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(TypeError):
            Rules()

        with self.assertRaises(TypeError):
            Rules(None)

        with self.assertRaises(TypeError):
            Rules("-/*")

        with self.assertRaises(TypeError):
            Rules("")

        self.assertIsInstance(Rules([]), Rules)

    def test_rules_to_str(self):
        args = [
            '-/*',
            '+/foo/',
            '-/proc/[0-9]*',
            '-/proc/[!a-z]*',
            '-*/.???*',
            '-[]^] [',
        ]
        rules = Rules(args)
        self.assertEqual(str(rules), "Rules({})".format(args))
