'''
Router
======

'''

import collections
import re

Field = collections.namedtuple('Field', ('namespace', 'regex'))
Result = collections.namedtuple('Result', ('namespace', 'name', 'match'))


class Router(object):
    '''Docker routes parsing methods

    Need to be initialized once, and rules set applied to it.
    '''
    _actions = {'GET', 'POST', 'DELETE', 'HEAD', 'PUT'}
    __data = None
    __r_namespace = re.compile(r'^([a-z]+)[A-Z][a-z][a-zA-Z]*$')

    def __init__(self):
        '''initialize object with default values
        '''
        self.__data = {
            k: {}
            for k in self._actions
        }

    def __repr__(self):
        return '<Router: {}>'.format(
            ', '.join(
                sorted(
                    '{}: {}'.format(k, len(v))
                    for k, v in self.__data.iteritems()
                )
            )
        )

    def register(self, method, pattern, action):
        '''register a rule set

        :param str method: one of :attr:`_actions`
        :param str pattern: regular expression
        :param str action: action name
        :raise: KeyError, ValueError
        '''
        try:
            namespace = self.__r_namespace.match(action).group(1)
        except AttributeError:
            raise ValueError(
                'bad format for action, '
                'unable to infer namespace from: {!r}'.format(action)
            )

        assert action not in self.__data[method]
        try:
            self.__data[method][action] = Field(
                namespace,
                re.compile(pattern),
            )
        except:
            raise ValueError(
                'unable to compile pattern: {!r}'.format(pattern)
            )

    def find(self, method, path):
        '''find the corresponding namespace and action name
        to a given method/path couple

        .. Note::
           The path (usually) **must not** contain the API version
           nor the query string.

        :param str method: HTTP method
        :param str path: path to match
        :rtype: Result
        :raise: ValueError
        '''
        for name, (namespace, regex) in self.__data[method].items():
            match = regex.match(path)
            if match:
                return Result(namespace, name, match.groups())
        raise ValueError(
            'no match for: {}: {}'.format(
                method,
                path,
            )
        )
