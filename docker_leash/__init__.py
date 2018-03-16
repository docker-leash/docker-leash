# vim:set ts=4 sw=4 et:
'''
A remote AuthZ plugin to enforce granular rules \
for a Docker multiuser environment

'''

import logging
import sys
sys.dont_write_bytecode = True

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler # Python 2.7+, see issue #97

from flask import Flask

__version__ = '0.0.1.dev0'

application = Flask(__name__)
application.config.from_object('config')

logging.getLogger(__name__).addHandler(NullHandler())
