#!/usr/bin/env python
# vim:set ts=4 sw=4 et:
'''
run
===
'''

from docker_leash.leash_server import application

if __name__ == '__main__':
    application.run(host="0.0.0.0")
