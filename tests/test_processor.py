# vim:set ts=4 sw=4 et:

import json
import unittest

from app.checks_list import Checks
from app.config import Config
from app.exceptions import UnauthorizedException
from app.payload import Payload
from app.processor import Processor

groups_allow = {
    'all': {
        'policies': ['allow'],
        'members': ['*']
    }
}

groups_deny = {
    'all': {
        'policies': ['deny'],
        'members': ['*']
    }
}

policies = {
    'allow': {
        'containersCreate': {
            'Allow': None
        }
    },
    'deny': {
        'containersCreate': {
            'Deny': None
        }
    }
}

mocked_body = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.32/containers/create",
    "RequestBody": "eyJmb28iOiAiYmFyIn0="  # '{"foo": "bar"}'
}


class ProcessorTests(unittest.TestCase):

    def test_init(self):
        Processor()

    def test_config_is_shared(self):
        processor1 = Processor()
        processor1.load_config()
        self.assertNotEqual(processor1.config, None)

        processor2 = Processor()
        processor2.load_config()
        self.assertNotEqual(processor2.config, None)

        # Now config should be the same on first object
        self.assertEqual(processor1.config, processor2.config)

        # TODO
        # processor2.config = Config(groups_allow, policies)
        # self.assertEqual(processor1.config, processor2.config)

    def test_run_with_no_checks(self):
        body = {}

        processor = Processor()
        with self.assertRaises(UnauthorizedException):
            processor.run(body=body)

    def test_override_config(self):
        processor = Processor()
        self.assertEqual(len(processor.config.groups), 3)
        self.assertEqual(len(processor.config.policies), 4)

        processor.config = Config(groups_allow, policies)
        self.assertEqual(len(processor.config.groups), 1)
        self.assertEqual(len(processor.config.policies), 2)

    def test_run_without_exception(self):
        processor = Processor()
        processor.config = Config(groups_allow, policies)
        processor.run(body=mocked_body)

    def test_run_simple_allow(self):
        processor = Processor()
        processor.config = Config(groups_allow, policies)
        processor.run(body=mocked_body)

    def test_run_simple_deny(self):
        processor = Processor()
        processor.config = Config(groups_deny, policies)
        with self.assertRaises(UnauthorizedException):
            processor.run(body=mocked_body)

    def test_run_simple_allow_as_string(self):
        processor = Processor()
        processor.config = Config(groups_allow, policies)
        processor.run(body=json.dumps(mocked_body))

    def test_run_simple_deny_as_string(self):
        processor = Processor()
        processor.config = Config(groups_deny, policies)
        with self.assertRaises(UnauthorizedException):
            processor.run(body=json.dumps(mocked_body))

    def test_process_simple_allow(self):
        payload = Payload(mocked_body)
        check = Checks()._structure_convert({"Allow": None})

        processor = Processor()
        processor._process(payload=payload, check=check)

    def test_process_simple_deny(self):
        payload = Payload(mocked_body)
        check = Checks()._structure_convert({"Deny": None})

        processor = Processor()
        with self.assertRaises(UnauthorizedException):
            processor._process(payload=payload, check=check)
