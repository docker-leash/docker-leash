# vim:set ts=4 sw=4 et:
'''
BindMounts
----------
'''

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


class BindMounts(BaseCheck):
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
        :type args: list or dict or str or None
        :param payload: The payload of the current request.
        :type payload: :class:`docker_leash.payload.Payload`
        """
        if not payload.data or \
            "RequestBody" not in payload.data or \
            "HostConfig" not in payload.data["RequestBody"] or \
            "Binds" not in payload.data["RequestBody"]["HostConfig"] or \
                not payload.data["RequestBody"]["HostConfig"]["Binds"]:
            return

        volumes = [value.split(':')[0] for value in payload.data["RequestBody"]["HostConfig"]["Binds"]]

        c_rules = Rules(args)
        denied = [
            volume
            for volume in volumes
            if not c_rules.match(volume)
        ]

        if not c_rules or denied:
            raise UnauthorizedException('unauthorized volumes: %s' % denied)


class Rules(object):
    __slots__ = ('rules', '__rules')
    suffix = r'(?:[\\/]|$)'

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
        rules = []
        for rule in self.rules:
            if not rule or rule[0] not in set('+-') or not rule[1:]:
                logging.warning('invalid rule: %r', rule)
                continue
            try:
                result += [(
                    rule[0] == '+',
                    re.compile(
                        rule[1:] + self.suffix,
                    ),
                    rule
                )]
                rules += [rule]
            except re.error as error:
                logging.warning('invalid rule: %r (%s)', rule, error)
        self.__rules = result
        self.rules = rules

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
