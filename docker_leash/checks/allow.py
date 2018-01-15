# vim:set ts=4 sw=4 et:

from .base import BaseCheck


class Allow(BaseCheck):
    """A simple module that say `yes`."""

    def run(self, config, payload):
        """Run the module checks.

        Say yes is easy, just dont raise any exception ;)

        :param config: The currently loaded configuration
        :type config: :class:`docker_leash.config.Config`
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        pass
