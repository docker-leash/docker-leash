# vim:set ts=4 sw=4 et:

"""Exceptions used in Docker Leash Server"""

class DockerLeashException(BaseException):
    """Base for all Leash Server Errors."""
    pass


class UnauthorizedException(DockerLeashException):
    """Exception for unauthorized action.

    All :mod:`app.checks` modules must return this exception in order to deny the action to the user.
    """

    def __init__(self, value):
        """Construct the exception

        :param string value: The human readable cause of the deny.
        """
        self.value = value

    def json(self):
        """Format the exception as dict object.

        :return: the exception as dict
        :rtype: dict
        """
        return {
            "Allow": False,
            "Msg": self.value
        }

    def __str__(self):
        return self.value


class NotForMeException(DockerLeashException):
    pass
