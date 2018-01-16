# vim:set ts=4 sw=4 et:

import logging
import os.path
import re

from ..exceptions import UnauthorizedException
from .base import BaseCheck

logger = logging.getLogger()

logging.basicConfig(
    format='%(levelname)s: %(message)s',
    datefmt='%F %T',
    level=logging.INFO,
    #    level=logging.DEBUG,
)


class BindVolumes(BaseCheck):
    """A module that checks mount binds from host filesystem"""

    def run(self, args, payload):
        """Run the module checks.

        Validate `volumes` against defined rules.
        Raise :exc:`UnauthorizedException` when one volume doesn't respect the rules.

        Rules examples:

        .. code-block:: yaml

            rules:
              - "-/"
              - "-/etc"
              - "+/0"
              - "-/home"
              - "+/home/$USER"
              - "+/home/devdata"

        :param args: The module arguments from the config
        :type args: list or dict or string or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        if not payload.data or \
            "RequestBody" not in payload.data or \
            "HostConfig" not in payload.data["RequestBody"] or \
            "Binds" not in payload.data["RequestBody"]["HostConfig"] or \
                not payload.data["RequestBody"]["HostConfig"]["Binds"]:
            return

        values = [value.split(':')[0] for value in payload.data["RequestBody"]["HostConfig"]["Binds"]]

        Proto()._check_path(values, args)


class Rules(object):
    __slots__ = ('rules', '__rules')

    def __init__(self, rules):
        self.rules = rules
        self.compile()

    def __str__(self):
        return 'Rules(%r)' % (
            self.rules,
        )

    def compile(self):
        if isinstance(self.rules, str):
            logging.warning('invalid rule: %r', self.rules)
            raise TypeError('Rules must be a list')

        result = []
        for rule in self.rules:
            if not rule or rule[0] not in set('+-'):
                logging.warning('invalid rule: %r', rule)
                continue
            result += [(
                rule[0] == '+',
                re.compile(
                    r'^%s(%s|$)' % (
                        self.translate(rule[1:]),
                        os.path.sep,
                    ),
                ),
                rule
            )]
        self.__rules = result

    @staticmethod
    def translate(pat):
        """Translate a shell PATTERN to a regular expression.

        There is no way to quote meta-characters.

        Copied and slightly modified from: :func:`fnmatch.translate`.
        """

        i, n = 0, len(pat)
        res = ''
        while i < n:
            c = pat[i]
            i = i + 1
            if c == '*':
                res = res + '.*'
            elif c == '?':
                res = res + '.'
            elif c == '[':
                j = i
                if j < n and pat[j] == '!':
                    j = j + 1
                if j < n and pat[j] == ']':
                    j = j + 1
                while j < n and pat[j] != ']':
                    j = j + 1
                if j >= n:
                    res = res + '\\['
                else:
                    stuff = pat[i:j].replace('\\', '\\\\')
                    i = j + 1
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    elif stuff[0] == '^':
                        stuff = '\\' + stuff
                    res = '%s[%s]' % (res, stuff)
            else:
                res = res + re.escape(c)
        return res

    def match(self, value):
        result = None
        value = os.path.normpath(value)
        for allow, regex, rule in self.__rules:
            match = regex.match(value)
            allowed = match and allow
            if match:
                result = allowed
            if __debug__:
                logger.debug('rule %r: %s: allow=%s', rule, result, allow)
        return result


class Proto(object):

    @staticmethod
    def _check_path(volumes, rules, user=None):
        """
        Validate `volumes` against defined rules.
        Raise :exc:`UnauthorizedException` when one volume doesn't respect the rules.

        Rules examples:

        .. code-block:: yaml

            rules:
              - -/
              - -/etc
              - +/0
              - -/home
              - +/home/$USER
              - +/home/devdata

        :param list volumes: list of path to check
        :param list rules: list of rules to check
        :param user: username or None
        :type user: str or bool
        """
        c_rules = Rules(rules)
        denied = [
            volume
            for volume in volumes
            if not c_rules.match(volume)
        ]

        if not c_rules or denied:
            raise UnauthorizedException('unauthorized volumes: %s' % denied)
