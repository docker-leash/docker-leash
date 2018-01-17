# vim:set ts=4 sw=4 et:
'''
Base
----
'''

import re


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

    @staticmethod
    def replace_user(value, payload):
        """A helper function to replace $USER in string

        If exact match is found, the replace is done by the value of the current
        connected user. If no user defined, then it return `None`. If '$' is
        preceded by a '\\' (backslash), then no substritituion is done.

        .. code-block:: pycon

            >>> payload = payload({"User": "mal"})
            >>> BaseCheck.replace_user("$USER-loves-me", payload)
            mal-loves-me

        .. code-block:: pycon

            >>> payload = payload({"User": "mal"})
            >>> BaseCheck.replace_user("\$USER-loves-me", payload)
            $USER-loves-me

        .. code-block:: pycon

            >>> payload = payload({"User": None})
            >>> BaseCheck.replace_user("$USER-loves-me", payload)
            # Return None

            >>> payload = payload({})
            >>> BaseCheck.replace_user("$USER-loves-me", payload)
            # Return None

        It works with `list` too:

        .. code-block:: pycon

            >>> a = ["who-loves-you", "$USER-loves-me", "\$USER-loves-me"]
            >>> payload = payload({"User": "mal"})
            >>> BaseCheck.replace_user("$USER-loves-me", payload)
            ["who-loves-you", "mal-loves-me", "\$USER-loves-me"]

        :param value: The input to replace
        :type value: string or list or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        :return: The replaced value(s)
        :rtype: string or list or None
        """

        def replace(value, new):
            return re.sub(
                r"(?<!\\)(?:\\\\)?\$USER",
                new,
                value
            )
            # return value.replace('$USER', new)

        if isinstance(value, str):
            if payload.user is None:
                return None
            return replace(value, payload.user)

        result = []
        for val in value:
            if payload.user is None:
                continue
            result.append(replace(val, payload.user))
        return result
