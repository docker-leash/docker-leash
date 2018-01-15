# vim:set ts=4 sw=4 et:

from ..exceptions import UnauthorizedException

from .base import BaseCheck


class Deny(BaseCheck):
    """A simple module that say `no`."""

    def run(self, config, payload):
        """Run the module checks.

        Say no is easy, just raise an :class:`UnauthorizedException` ;)

        :param config: The currently loaded configuration
        :type config: :class:`docker_leash.config.Config`
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        raise UnauthorizedException("Operation denied by configuration.")
