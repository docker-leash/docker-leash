# vim:set ts=4 sw=4 et:
'''
ReadOnly
--------
'''

from ..action_mapper import Action
from ..exceptions import UnauthorizedException
from .base import BaseCheck


class ReadOnly(BaseCheck):
    """A module that check if the current action is read-only
    """

    def run(self, args, payload):
        """Run the module checks.

        If the current action is not a `GET` or `HEAD` request (i.e.: read-only),
        then :exc:`docker_leash.exceptions.UnauthorizedException` is raised.

        :param args: The module arguments from the config
        :type args: None
        :param docker_leash.payload.Payload payload: payload of the current
                                                     request
        """
        mapper = Action(method=payload.method, query=payload.uri)
        if mapper.is_readonly():
            return

        raise UnauthorizedException("Operations are restricted to read-only.")
