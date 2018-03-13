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

        If the requested action should be forbidden then the module must raise
        an :exc:`docker_leash.exceptions.UnauthorizedException`.

        .. Warning::
           This function *must* be overridden in each check modules.

        :param args: The module arguments, from the configuration
        :type args: list or dict or str or None
        :param docker_leash.payload.Payload payload: payload of the current request
        """
        raise NotImplementedError(
            "'run' mot implemented in module `%s`" % self.__class__.__name__
        )

    @staticmethod
    def replace_user(value, payload):
        r"""A helper function to replace $USER in string

        If exact match is found, the replace is done by the value of the current
        connected user. If no user defined, then it return `None`. If '$' is
        preceded by a ``\`` (backslash), then no substitution is done.

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

        def replace(value, user):
            """Replace $USER if necessary
            """
            if re.search(r'((?<!\\)(?:\\\\)*)\$USER', value):
                if not user:
                    return None
                return re.sub(
                    r'((?<!\\)(?:\\\\)*)\$USER',
                    r'\1' + user,
                    value
                )
            return value

        if isinstance(value, str):
            return replace(value, payload.user)

        result = []
        for val in value:
            replaced = replace(val, payload.user)
            if replaced is not None:
                result.append(replaced)
        return result
