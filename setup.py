#!/usr/bin/env python
'''
Description
-----------

A remote AuthZ_ plugin to enforce granular rules for a Docker multiuser
environment.

Have you ever wanted to restrict users on your system to manage
only certain containers?
Did you ever wanted to restrict witch path can be bind mounted?
Did you ever wanted to log every commands run by your users?
If 'yes', then ``docker-leash`` is for you.

Docker Leash is a centralized point for managing authorization
for your docker daemon.
It is distributed as a web application backed by Flask_.

.. _AuthZ: https://docs.docker.com/engine/extend/plugins_authorization/
.. _Flask: http://flask.pocoo.org/
'''

# stdlib
import io
import re

# dependencies
from setuptools import setup

version = None
with io.open('docker_leash/leash_server.py', 'rt', encoding='utf8') as fobj:
    version = re.search(
        r'''__version__\s*=\s*(?P<q>["'])(.*)(?P=q)''',
        fobj.read(),
        re.M,
    ).group(2)

_github_path = 'docker-leash/leash-server'



setup(
    name='docker-leash',
    version=version,
    author='Mathieu Alorent',
    author_email='docker-leash@kumy.net',
    description='Docker authorization plugin',
    long_description=__doc__,
    license='MIT',
    keywords=['docker', 'authz', 'authorization'],
    url='https://github.com/{}'.format(_github_path),
    download_url='https://api.github.com/repos/{}/tarball/{}'.format(
        _github_path,
        version or ''
    ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Systems Administration',
    ],
    packages=[
        'docker_leash',
    ],
    package_data={
        '': ['*.yml']
    },
    platforms='any',
    py_modules=(
    ),
    install_requires=[
        'Flask>=0.12',
        'PyYAML',
    ],
    test_suite='tests',
)
