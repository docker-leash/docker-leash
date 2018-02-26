# vim:set ts=4 sw=4 et:
'''
Privileged
----------
'''

from ..exceptions import UnauthorizedException
from .base import BaseCheck


class Privileged(BaseCheck):
    """Check respect of the `privileged` flag
    """

    def run(self, args, payload):
        """Run the module checks.

        When used, container creation should have the `Privileged` flag set to
        `False`, or be absent.

        :param args: The module arguments from the config
        :type args: None
        :param docker_leash.payload.Payload payload: payload of the current request
        """
        if not payload.data or \
            "RequestBody" not in payload.data or \
            "HostConfig" not in payload.data["RequestBody"] or \
            "Privileged" not in payload.data["RequestBody"]["HostConfig"] or \
                not payload.data["RequestBody"]["HostConfig"]["Privileged"]:
            return
        raise UnauthorizedException("Operation denied by configuration.")
