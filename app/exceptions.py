# vim:set ts=4 sw=4 et:


class DockerLeashException(BaseException):
    pass


class UnauthorizedException(DockerLeashException):
    def __init__(self, value):
        self.value = value

    def json(self):
        return {
            "Allow": False,
            "Msg": self.value
        }

    def __str__(self):
        return self.value


class NotForMeException(DockerLeashException):
    pass
