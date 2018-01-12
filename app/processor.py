# vim:set ts=4 sw=4 et:

import base64
import json

import yaml

import app.checks as checks
from app.action_mapper import ActionMapper
from app.config import Config
from app.exceptions import UnauthorizedException
from app.leash_server import app
from app.payload import Payload


class Processor():

    # Mutable properties
    config = Config()

    def __init__(self):
        pass

    def load_config(self):
        with open(app.config['GROUPS_FILE']) as g, open(app.config['POLICIES_FILE']) as p:
            groups = yaml.load(g)
            policies = yaml.load(p)

        self.config.update(groups, policies)

    def run(self, body=None):
        data = json.loads(body) if type(body) is str else body

        payload = Payload(data)
        action = ActionMapper().get_action_name(method=payload.method, uri=payload.uri)

        if action is None:
            raise UnauthorizedException("Forbidden by default when no action specified.")

        checks = self.config.get_checks_for_user(payload.user, action)

        if not checks:
            raise UnauthorizedException("Forbidden by default when no checks specified (%s)." % action)

        for check in checks:
            self._process(payload, check)

    def _process(self, payload, check):
        check_action = getattr(checks, check['name'])()
        check_action.run(self.config, payload)
