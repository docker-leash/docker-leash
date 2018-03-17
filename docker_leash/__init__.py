# vim:set ts=4 sw=4 et:
'''
A remote AuthZ plugin to enforce granular rules \
for a Docker multiuser environment

'''

import sys
sys.dont_write_bytecode = True

from flask import Flask

__version__ = '0.0.1.dev0'

app = Flask(__name__)
app.config.from_object('config')
