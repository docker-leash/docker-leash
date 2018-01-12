# vim:set ts=4 sw=4 et:

from app.exceptions import UnauthorizedException

from .base import BaseCheck


class Deny(BaseCheck):

    def run(self, config, payload):
        raise UnauthorizedException("Operation denied by configuration.")
