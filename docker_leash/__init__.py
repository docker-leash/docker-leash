# vim:set ts=4 sw=4 et:
'''
A remote AuthZ plugin to enforce granular rules \
for a Docker multiuser environment

'''

import logging
import sys

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler # Python 2.7+, see issue #97

import flask

__version__ = '0.0.1.dev0'

application = flask.Flask(__name__)  # pylint: disable=C0103
application.config.from_object('config')

logging.getLogger(__name__).addHandler(NullHandler())
