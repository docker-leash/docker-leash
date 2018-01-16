# vim:set ts=4 sw=4 et:

import json

import yaml

from . import checks
from .action_mapper import ActionMapper
from .config import Config
from .exceptions import NoSuchCheckModuleException, UnauthorizedException
from .leash_server import app
from .payload import Payload


class Processor(object):
    """The :class:`Processor` class is responsible for launching all the :mod:`docker_leash.checks` defined in the configuration for
    the triplet `User`, `RequestMethod` and `RequestUri`.
    """

    # Mutable properties
    #: The currently loaded rules.
    config = Config()

    def load_config(self):
        """Load rules from defined files in the global configuration."""
        with open(app.config['GROUPS_FILE']) as g, open(app.config['POLICIES_FILE']) as p:
            groups = yaml.load(g)
            policies = yaml.load(p)

        self.config.update(groups, policies)

    def run(self, body=None):
        """Check if the request is `accepted` or `denied`.

        The request will be passed to all configured :mod:`docker_leash.checks` for the triplet :class:`Payload.user` +
        :class:`Payload.method` + :class:`Payload.uri`.
        If one :mod:`docker_leash.checks` deny the action, then the whole request is declared as `denied`.

        :param body: The http request body
        :type body: string or dict or None
        :raises UnauthorizedException: if no rule is defined, or if the check deny the request.
        """
        data = json.loads(body) if isinstance(body, str) else body

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
        """Instanciate the requested action and launch the :class:`docker_leash.checks.base.run()` method.

        :param payload: The request payload object.
        :type payload: :class:`Payload`
        :param string check: The check name to run.
        :raises UnauthorizedException: if the check deny the request.
        """
        try:
            check_action = getattr(checks, check['name'])()
        except AttributeError as e:
            raise NoSuchCheckModuleException("Check module '%s' does not exists or not autoloadable." % check['name'])
        check_action.run(check['args'], payload)
