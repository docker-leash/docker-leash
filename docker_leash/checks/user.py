# vim:set ts=4 sw=4 et:
'''
User
----
'''

import re

from ..exceptions import ConfigurationException, UnauthorizedException
from .base import BaseCheck


class User(BaseCheck):
    """A module that checks the user the container run as"""

    def run(self, args, payload):
        """Run the module checks.

        Validate `user name` against defined rules.
        Raise :exc:`UnauthorizedException` when the user name doesn't
        respect the rules.

        When a list is given, Exception is raised only if all rules fails.

        If no name was forced for the container creation, then authorization is
        granted.

        Rules examples:

        .. code-block:: yaml

            rules: "^someone$"

        .. code-block:: yaml

            rules: "^$USER$"

        .. code-block:: yaml

            rules: "^bot-.+$"

        Or a list:

        .. code-block:: yaml

            rules: ["^some_name$", "^$USER$"]

        :param args: The module arguments from the config
        :type args: list or dict or str or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        if not args:
            raise ConfigurationException(
                'Incomple "User" module configuration'
            )

        name = self._get_name(payload)
        if name is None:
            return

        rules = args if isinstance(args, list) else [args]
        rules = self.replace_user(rules, payload)

        for rule in rules:
            if re.match(rule, name):
                return

        raise UnauthorizedException(
            'User name verification failed: user name breaks the rules'
        )

    @staticmethod
    def _get_name(payload):
        """Return the user name from payload

        :param Payload payload: The current payload
        :return: The user name
        :rtype: str or None
        """

        if not payload.data or \
            "RequestBody" not in payload.data or \
            "User" not in payload.data["RequestBody"] or \
                not payload.data["RequestBody"]["User"]:
            return None

        return payload.data["RequestBody"]["User"]
