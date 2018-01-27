# vim:set ts=4 sw=4 et:
'''
Processor
=========
'''

import json
import os

import yaml

from . import app, checks
from .config import Config
from .exceptions import NoSuchCheckModuleException
from .payload import Payload


class Processor(object):
    """The :class:`Processor` class is responsible for launching all the
    :mod:`docker_leash.checks` defined in the configuration for
    the triplet `User`, `RequestMethod` and `RequestUri`.
    """

    #: The currently loaded rules.
    config = None

    def __init__(self):
        self.config = Config()

    def load_config(self):
        """Load rules from defined files in the global configuration.

        Look for path in that order: path in config file, `/etc/docker-leash/`,
        `/config/` and docker-leash module directory.
        """

        groups_files = [
            app.config['GROUPS_FILE'],
            '/etc/docker-leash/groups.yml',
            '/config/groups.yml',
            os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + '/../groups.yml'
            ),
        ]
        policies_files = [
            app.config['POLICIES_FILE'],
            '/etc/docker-leash/policies.yml',
            '/config/policies.yml',
            os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + '/../policies.yml'
            ),
        ]

        groups = None
        for groups_file in groups_files:
            if os.path.isfile(groups_file):
                app.logger.info("Found groups config at: %s", groups_file)
                with open(groups_file) as groups_yml:
                    groups = yaml.safe_load(groups_yml)
                    break

        policies = None
        for policies_file in policies_files:
            if os.path.isfile(policies_file):
                app.logger.info("Found policies config at: %s", policies_file)
                with open(policies_file) as policies_yml:
                    policies = yaml.safe_load(policies_yml)
                    break

        self.config.update(groups, policies)

    def run(self, body=None):
        """Check if the request is `accepted` or `denied`.

        The request will be passed to all configured :mod:`docker_leash.checks`
        for the triplet :attr:`docker_leash.payload.Payload.user` +
        :attr:`docker_leash.payload.Payload.method` +
        :attr:`docker_leash.payload.Payload.uri`.
        If one :mod:`docker_leash.checks` sub-modules deny the action,
        then the whole request is declared as `denied`.

        :param body: The HTTP request body
        :type body: str or dict or None
        :raises UnauthorizedException: if the check denied the request.
        :raises NoSuchCheckModuleException: if the check doesn't exists.
        """
        data = json.loads(body) if isinstance(body, str) else body

        payload = Payload(data)

        checks_for_user = self.config.get_rules(payload)
        for check in checks_for_user:
            self._process(payload, check)

    @staticmethod
    def _process(payload, check):
        """Instanciate the requested action and launch
        :meth:`docker_leash.checks.base.BaseCheck.run`

        :param Paylod payload: The request payload object.
        :param str check: The check name to run.
        :raises UnauthorizedException: if the check denied the request.
        :raises NoSuchCheckModuleException: if the check doesn't exists.
        """
        try:
            check_action = getattr(checks, check['name'])()
        except AttributeError:
            raise NoSuchCheckModuleException(
                "Check module '%s' does not exists or not autoloadable." %
                check['name']
            )
        check_action.run(check['args'], payload)
