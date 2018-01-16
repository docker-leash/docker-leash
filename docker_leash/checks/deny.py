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

        Say no is easy, just raise an :exception:`UnauthorizedException` ;)

        :param args: The module arguments from the config
        :type args: list or dict or string or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        raise UnauthorizedException("Operation denied by configuration.")
