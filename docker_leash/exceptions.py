# vim:set ts=4 sw=4 et:
"""Exceptions used in Docker Leash Server
"""


class DockerLeashException(BaseException):
    """Base for all Leash Server Errors."""

    def __init__(self, value=None):
        """Construct the exception

        :param str value: The human readable cause of the deny.
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


class UnauthorizedException(DockerLeashException):
    """Exception for unauthorized action.

    All :mod:`docker_leash.checks` modules must return this exception
    in order to deny the action to the user.
    """
    pass


class NoSuchCheckModuleException(DockerLeashException):
    """Exception for non existent check module.

    Used when a check is configured by not existent or loadable.
    """
    pass


class ConfigurationException(DockerLeashException):
    """Exception for configuration errors.

    Used when configuration files are invalid.
    """
    pass


class InvalidRequestException(DockerLeashException):
    """Exception for invalid payload.

    Used when payload is invalid or incomplete.
    """
    pass
