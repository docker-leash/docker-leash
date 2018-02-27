# vim:set ts=4 sw=4 et:
'''
ContainerName
-------------
'''

import re
from urlparse import parse_qs, urlsplit

from ..action_mapper import ActionMapper
from ..exceptions import UnauthorizedException
from .base import BaseCheck


def query_parameter(payload, parameter_name="name"):
    """Extract container name from the query parameters
    """
    query = parse_qs(urlsplit(payload.uri).query)

    if parameter_name not in query:
        return ""

    return query[parameter_name][0]


def path_parameter(payload):
    """Extract container name from the path parameters
    """
    path = urlsplit(payload.uri).path
    match = re.match(r"^/v\d.\d{2}/[^/]+/([a-zA-Z0-9_-]+)/?", path)

    if match is None:
        raise UnauthorizedException(
            'Container name not found in path'
        )
    return match.group(1)


FUNCTION_MAP = {
    'containersCreate': query_parameter,
    'containersInspect': path_parameter,
    'containersListProcess': path_parameter,
    'containersLogs': path_parameter,
    'containersChanges': path_parameter,
    'containersExport': path_parameter,
    'containersStats': path_parameter,
    'containersAttachWebsocket': path_parameter,
    'containersGetFilesystemArchive': path_parameter,
    'containersRemove': path_parameter,
    'containersResizeTTY': path_parameter,
    'containersStart': path_parameter,
    'containersStop': path_parameter,
    'containersRestart': path_parameter,
    'containersKill': path_parameter,
    'containersUpdate': path_parameter,
    'containersRename': path_parameter,  # TODO check old and new name
    'containersPause': path_parameter,
    'containersUnpause': path_parameter,
    'containersAttach': path_parameter,
    'containersWait': path_parameter,
    'containersPrune': path_parameter,
    'containersExtractArchiveToDirectory': path_parameter,
    'containersGetInfoAboutFiles': path_parameter,
    'containersPrune': path_parameter,  # TODO it use filter, should be parsed
                                        # in in authZ.Req
    'networksConnect': path_parameter,
    'networksDisconnect': path_parameter,
    'execCreate': path_parameter,
    'execInspect': path_parameter,
    'execStart': path_parameter,
    'execResize': path_parameter,
}


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

        name = self._get_name(payload)
        if name is None:
            return

        found = False
        rules = args if isinstance(args, list) else [args]
        rules = self.replace_user(rules, payload)

        for rule in rules:
            if re.match(rule, name):
                found = True

        if not found:
            raise UnauthorizedException(
                'Container name verification failed: container name breaks the rules'
            )

    @staticmethod
    def _get_name(payload):
        """Return the name of the container

        :param Payload payload: The current payload
        :return: The container name
        :rtype: str or None
        """
        action = ActionMapper().get_action_name(method=payload.method, uri=payload.uri)
        if action not in FUNCTION_MAP:
            return None

        return FUNCTION_MAP[action](payload)
