# vim:set ts=4 sw=4 et:
'''
ImageName
---------
'''

import logging
import re
try:
    from urllib.parse import parse_qs, urlsplit
except ImportError:
    # python2
    from urlparse import parse_qs, urlsplit

from ..action_mapper import Action
from ..exceptions import (ConfigurationException, InvalidRequestException,
                          UnauthorizedException)
from .base import BaseCheck


def query_parameter(payload, **kwargs):
    """Extract image name from the query parameters
    """
    parameter_name = kwargs.get('parameter_name', 't')
    query = parse_qs(urlsplit(payload.uri).query)
    logging.debug('Query parameters: %s', query)

    if parameter_name not in query:
        raise InvalidRequestException(
            'Image name not found in query parameters'
        )

    response = []
    for image in query[parameter_name]:
        if ':' in image:
            name, tag = image.split(':')
        else:
            name = image
            tag = 'latest'
        if len(query[parameter_name]) == 1:
            return (name, tag)
        response.append((name, tag))
    return response


def query_parameter_compound(payload, **kwargs):
    """Extract image name from the query parameters
    """
    parameter_name = kwargs.get('parameter_name', 'repo')
    parameter_tag = kwargs.get('parameter_tag', 'tag')

    query = parse_qs(urlsplit(payload.uri).query)

    if parameter_name not in query:
        raise InvalidRequestException(
            'Image name not found in query parameters'
        )
    name = query[parameter_name][0]

    if parameter_tag in query:
        tag = query[parameter_tag][0]
    else:
        tag = 'latest'

    return (name, tag)


def path_and_query_parameter(payload, **kwargs):
    """Extract image name from path, tag from the query parameters
    """
    # Extract name
    path = urlsplit(payload.uri).path
    match = re.match(
        r"^/v\d.\d{2}/[^/]+/([a-zA-Z0-9/:_.-]+)(/(json|tag|history|push|get))+/?",
        path)
    name = match.group(1)

    # Extract tag
    parameter_tag = kwargs.get('parameter_tag', 'tag')
    query = parse_qs(urlsplit(payload.uri).query)

    if parameter_tag not in query:
        raise InvalidRequestException(
            'Image tag not found in query parameters'
        )
    tag = query[parameter_tag][0]

    return (name, tag)


#pylint: disable=unused-argument
def path_parameter(payload, **kwargs):
    """Extract container name from the path parameters
    """
    path = urlsplit(payload.uri).path
    if payload.method == "DELETE":
        match = re.match(r"^/v\d.\d{2}/[^/]+/([a-zA-Z0-9/:_.-]+)/?", path)
    else:
        match = re.match(
            r"^/v\d.\d{2}/[^/]+/([a-zA-Z0-9/:_.-]+)(/(json|tag|history|push|get))+/?",
            path)

    if ':' in match.group(1):
        name, tag = match.group(1).split(':')
    else:
        name = match.group(1)
        tag = 'latest'
    return (name, tag)


def source_and_dest(payload, **kwargs):
    """Extract image name from the path and query parameters
    """
    (src_name, src_tag) = path_parameter(payload, **kwargs)
    (dst_name, dst_tag) = query_parameter_compound(payload, **kwargs)
    return [(src_name, src_tag), (dst_name, dst_tag)]


FUNCTION_MAP = {
    # 'imagesList': query_filter_parameter, # ignored right now
    'imagesBuild': (query_parameter, {"parameter_name": "t"}),
    'imagesCreate': [
        (query_parameter, {"parameter_name": "repo"}),  # import
        (query_parameter_compound, {"parameter_name": "fromImage", "parameter_tag": "tag"}),  # pull
    ],
    'imagesInspect': path_parameter,
    'imagesHistory': path_parameter,
    'imagesPush': path_and_query_parameter,
    'imagesTag': [
        (source_and_dest, {"parameter_name": "repo", "parameter_tag": "tag"}),
    ],
    'imagesRemove': path_parameter,
    'imagesCommit': [
        (query_parameter_compound, {"parameter_name": "repo", "parameter_tag": "tag"}),
    ],
    'imagesExport': path_parameter,
    'imagesExportMultiple': (query_parameter, {"parameter_name": "names"}),
}


def get_action_name(payload, action_name=None):
    """Return the action_name for the Payload URI

    :param Payload payload: The current payload
    :return: The action_name
    :rtype: str or None
    """
    if action_name is None:
        action_name = Action(method=payload.method, query=payload.uri).name
        if action_name not in FUNCTION_MAP:
            return None
    return action_name


class ImageName(BaseCheck):
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
            raise ConfigurationException(
                'Incomplete "ImageName" module configuration'
            )

        name = get_action_name(payload)
        if name is None:
            return

        names = self._get_name(payload, name)

        rules = args if isinstance(args, list) else [args]
        rules = self.replace_user(rules, payload)
        logging.debug('Rules: %s', rules)

        for rule in rules:
            for image_name in names:
                if not re.match(rule, image_name[0]):
                    raise UnauthorizedException(
                        'Image name not authorized'
                    )

    @staticmethod
    def _get_name(payload, action_name=None):
        """Return the name of the container

        :param Payload payload: The current payload
        :return: The container name
        :rtype: str or None
        """
        def call(function, payload):
            """Called function is optional
            """
            if isinstance(function, tuple):
                function_name = function[0]
                kwargs = function[1]
            else:
                function_name = function
                kwargs = {}

            return function_name(payload, **kwargs)

        action_name = get_action_name(payload, action_name)
        function = FUNCTION_MAP[action_name]

        # Multiple rules
        if isinstance(function, list):
            for item in function:
                try:
                    return call(item, payload)
                except InvalidRequestException:
                    pass
            raise InvalidRequestException(
                'Action name not found: %s' % action_name
            )

        # Single rule
        return call(function, payload)
