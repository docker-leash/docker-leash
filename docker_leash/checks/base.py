# vim:set ts=4 sw=4 et:
'''
Base
----
'''


class BaseCheck(object):
    """The :class:`BaseCheck` class is the base class for all the checks
    """

    def run(self, args, payload):
        """Run the module checks.

        The implemented check module receive the global configuration and
        the current payload.
        It is autonomous in how the checks are implemented.

        If the requested action shoudl be forbiddenm then the module must raise
        a :exception:`UnauthorizedException`.

        .. Warning::
           This function *must* be overrided in each check modules.

        :param args: The module arguments from the config
        :type args: list or dict or string or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        raise NotImplementedError(
            "'run' mot implemented in module `%s`" % self.__class__.__name__
        )
