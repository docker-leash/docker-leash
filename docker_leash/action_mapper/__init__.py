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
        if self.__namespace:
            return self.__namespace

        raise NotImplementedError  # TODO: init namespace
        '''
        Something like:
        self.__namespace = Container(action=self)
        '''

        return self.__namespace

    def _parse(self):
        '''
        :raise: InvalidRequestException
        '''
        try:
            result = self._r_parse.match(self.query).groupdict()
        except AttributeError:
            raise InvalidRequestException(
                'unable to parse: {}'.format(self.query)
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
