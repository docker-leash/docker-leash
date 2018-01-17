# vim:set ts=4 sw=4 et:

'''
Deny
----
'''

from ..exceptions import UnauthorizedException
from .base import BaseCheck


class Deny(BaseCheck):
    """A simple module that say `no`
    """

    def run(self, args, payload):
        """Run the module checks.

        Saying no is easy, just raise an
        :exc:`docker_leash.exceptions.UnauthorizedException` ;^)

        :param args: The module arguments from the config
        :type args: list or dict or str or None
        :param docker_leash.payload.Payload payload: payload of the current request
        """
        raise UnauthorizedException("Operation denied by configuration.")
