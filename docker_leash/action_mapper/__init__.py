'''
Action
======
'''

import re
import urlparse

from ..exceptions import InvalidRequestException
from .routes import routes


class Action(object):
    '''
    :var method: HTTP method used
    :var query: unparsed query
    :var name: parsed name (i.e.: containersList, imagesBuild, ...)
    :var version: API version call, if present
    :var querystring: parsed querystring
    :var namespace_name: (i.e.: containers, images, ...)
    '''
    # raw data
    method = None
    query = None
    # one parsed
    name = None
    namespace_name = None
    version = None
    querystring = None

    _namespace_map = {}
    __namespace = None
    _r_parse = re.compile(
        r'''
        ^(
            (?:/v(?P<version>[0-9.]+))?
            (?P<unparsed>/.*?)?
            (?:[?](?P<qs>.*?))?
            (?:[#](?P<fragment>.*))?
        )$
        ''',
        re.X
    )

    def __init__(self, method, query):
        '''
        :param str method: uppercase HTTP method of the request
        :param str query: path and optional query string
        :raise: InvalidRequestException
        '''
        self.method = method
        self.query = query
        try:
            self._parse()
        except Exception as error:
            raise InvalidRequestException(
                error.message,
            )

    def is_readonly(self):
        '''Can the action affect the state of a resource.

        :rtype: bool
        '''
        return self.method in {'GET', 'HEAD'}

    @property
    def namespace(self):
        '''Initialize and return a Namespace object when required

        :rtype: Namespace instance
        '''
        if self.__namespace:
            return self.__namespace

        self.__namespace = self._namespace_map.get(
            self.namespace_name,
            Namespace,
        )(self)

        return self.__namespace

    def _parse(self):
        '''
        :raise: InvalidRequestException
        '''
        try:
            result = self._r_parse.match(self.query).groupdict()
        except AttributeError:
            raise InvalidRequestException(
                'unable to parse query: {}'.format(self.query)
            )

        self.version = result['version']
        if result['qs']:
            self.querystring = urlparse.parse_qs(result['qs'])

        try:
            result = routes.find(self.method, result['unparsed'])
        except ValueError as error:
            raise InvalidRequestException(
                'unable to parse query: {}, error: {}'.format(
                    self.query,
                    error.message,
                )
            )
        self.namespace_name = result.namespace
        self.name = result.name
        self.match = result.match

    def __repr__(self):
        return 'Action({!r}, {!r})'.format(
            self.method,
            self.query,
        )

    @classmethod
    def namespace_register(cls, arg):
        '''A decorator to register Namespace
        for a given namespace name

        If no namespace name is provided,
        it will be derivated from the class name.

        :param Action cls:
        :param arg:
        :type arg: str or Namespace instance
        '''
        def register(obj):
            '''internal function for the decorator
            '''
            assert arg not in cls._namespace_map
            cls._namespace_map[arg] = obj
            return obj

        if hasattr(arg, '__bases__'):
            arg, obj = arg.__name__.lower(), arg
            return register(obj)

        return register


class Namespace(object):
    '''Generic namespace

    :var action: link to (parent) action
    '''
    action = None

    def __init__(self, action):
        '''Initialize the object
        '''
        assert isinstance(action, Action)
        self.action = action


@Action.namespace_register('images')
class Image(Namespace):
    '''Proof of concept for Namespace subclasses
    '''

    def names(self):
        '''
        :rtype: list or None
        '''
        return self.action.querystring.get('names')


@Action.namespace_register('containers')
class Container(Namespace):
    '''Proof of concept for Namespace subclasses
    '''

    def names(self):
        '''
        :rtype: list or None
        '''
        # Those actions may contain name in querystring
        actions = [
            'containersCreate',
            'containersRename',
        ]
        names = []
        if self.action.match:
            names.append(self.action.match[0])
        if self.action.querystring:
            names.extend(self.action.querystring.get('name'))

        if not names and self.action.name in actions:
            # if no name provided at all for an action that may contain name
            # then declare an empty string
            names.append('')
        return names
