# vim:set ts=4 sw=4 et:
'''
ContainerName
-------------
'''

import re

from ..action_mapper import Action
from ..exceptions import UnauthorizedException
from .base import BaseCheck


class ContainerName(BaseCheck):
    """A module that checks the container name"""

    def run(self, args, payload):
        """Run the module checks.

        Validate `container name` against defined rules.
        Raise :exc:`UnauthorizedException` when the container name doesn't
        respect the rules.

        When a list is given, Exception is raised only if all rules fails.

        If no name was forced for the container creation, then Exception is
        raised.

        Rules examples:

        .. code-block:: yaml

            rules: "^myproject-.*$"

        .. code-block:: yaml

            rules: "^$USER-.*$"

        .. code-block:: yaml

            rules: "^only_this_container_name$"

        Or a list:

        .. code-block:: yaml

            rules: ["^only_this_container_name$", "^$USER-.*$"]

        The container name used on Request is contained in the uri query
        parameters as 'name'.

        :param args: The module arguments from the config
        :type args: list or dict or str or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        if not args:
            # Probably an error, raiseConfigError?
            return

        action = Action(
            payload.method,
            payload.uri,
        )
        names = action.namespace.names()
        # Some action dont contain name at all
        if not names:
            return

        rules = args if isinstance(args, list) else [args]
        rules = self.replace_user(rules, payload)

        found = False
        for rule in rules:
            for name in names:
                if re.match(rule, name):
                    found = True

        if not found:
            raise UnauthorizedException(
                'Container name verification failed: container name breaks the rules'
            )
