# vim:set ts=4 sw=4 et:

from .base import BaseCheck


class Allow(BaseCheck):
    """A simple module that say `yes`."""

    def run(self, args, payload):
        """Run the module checks.

        Say yes is easy, just dont raise any exception ;)

        :param args: The module arguments from the config
        :type args: list or dict or string or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        pass
