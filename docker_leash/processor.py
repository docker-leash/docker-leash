# vim:set ts=4 sw=4 et:
'''
Processor
=========
'''

import json

import yaml

from . import app, checks
from .action_mapper import ActionMapper
from .config import Config
from .exceptions import NoSuchCheckModuleException, UnauthorizedException
from .payload import Payload


class Processor(object):
    """The :class:`Processor` class is responsible for launching all the
    :mod:`docker_leash.checks` defined in the configuration for
    the triplet `User`, `RequestMethod` and `RequestUri`.
    """

    # Mutable properties
    #: The currently loaded rules.
    config = Config()

    def load_config(self):
        """Load rules from defined files in the global configuration."""
        with open(app.config['GROUPS_FILE']) as groups_file, \
             open(app.config['POLICIES_FILE']) as policies_file:
            groups = yaml.safe_load(groups_file)
            policies = yaml.safe_load(policies_file)

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
        :raises UnauthorizedException: if no rule is defined,
                                       or if the check deny the request.
        """
        data = json.loads(body) if isinstance(body, str) else body

        payload = Payload(data)
        action = ActionMapper().get_action_name(method=payload.method, uri=payload.uri)

        if action is None:
            raise UnauthorizedException(
                "Forbidden by default when no action specified."
            )

        checks_for_user = self.config.get_checks_for_user(payload.user, action)

        if not checks_for_user:
            raise UnauthorizedException(
                "Forbidden by default when no checks specified (%s)." % action
            )

        for check in checks_for_user:
            self._process(payload, check)

    @staticmethod
    def _process(payload, check):
        """Instanciate the requested action and launch
        :meth:`docker_leash.checks.base.BaseCheck.run`

        :param Paylod payload: The request payload object.
        :param str check: The check name to run.
        :raises UnauthorizedException: if the check deny the request.
        """
        try:
            check_action = getattr(checks, check['name'])()
        except AttributeError:
            raise NoSuchCheckModuleException("Check module '%s' does not exists or not autoloadable." % check['name'])
        check_action.run(check['args'], payload)
