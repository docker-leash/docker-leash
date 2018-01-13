# vim:set ts=4 sw=4 et:


class BaseCheck():
    """The :class:`app.action_mapper.BaseCheck` class is the base class for all the checks."""

    def run(self, config, payload):
        """Run the module checks.

        The implemented check module receive the global configuration and the current payload. It is autonomous in how
        the checks are implemented.

        If the requested action shoudl be forbiddenm then the module must raise a :class:`UnauthorizedException`.

        .. warning::
           This function *must* be overrided in each check modules.

        :param config: The currently loaded configuration
        :type config: :class:`app.config.Config`
        :param payload: The payload of the current request.
        :type payload: :class:`app.payload.Payload`
        """
        raise NotImplementedError(
            "'run' mot implemented in module `%s`" % self.__class__.__name__
        )
