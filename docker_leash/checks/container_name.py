# vim:set ts=4 sw=4 et:

'''
ContainerName
----
'''

import re
from urlparse import parse_qs, urlsplit

from ..exceptions import UnauthorizedException
from .base import BaseCheck


class ContainerName(BaseCheck):
    """A module that checks the container name"""

    def run(self, args, payload):
        """Run the module checks.

        Validate `container name` against defined rules.
        Raise :exc:`UnauthorizedException` when the container name doesn't
        respect the rules.

        Rules examples:

        .. code-block:: yaml

            rules: "^myproject-.*$"

        .. code-block:: yaml

            rules: "^$USER-.*$"

        .. code-block:: yaml

            rules: "^only_this_container_name$"

        The container name used on Request is contained in the uri query
        parameters as 'name'.

        :param args: The module arguments from the config
        :type args: list or dict or string or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """

        if not payload.uri:
            raise UnauthorizedException(
                'Container name verification failed: uri not found')

        if not args:
            return

        query = parse_qs(urlsplit(payload.uri).query)

        if 'name' not in query:
            raise UnauthorizedException(
                'Container name verification failed: container name not found'
            )

        for name in query['name']:
            if not re.match(args, name):
                raise UnauthorizedException(
                    'Container name verification failed: container name breaks the rules'
                )
