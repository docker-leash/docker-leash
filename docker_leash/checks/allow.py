# vim:set ts=4 sw=4 et:
'''
Allow
-----
'''

from .base import BaseCheck


class Allow(BaseCheck):
    """A simple module that say `yes`."""

    def run(self, args, payload):
        """Run the module checks.

        Saying *yes* is easy: just do not raise any exception ;^)

        :param args: The module arguments from the config
        :type args: list or dict or str or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        pass
