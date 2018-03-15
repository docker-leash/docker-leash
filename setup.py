#!/usr/bin/env python
'''
setup.py
========
'''

# stdlib
import io
import re

# dependencies
from setuptools import setup

VERSION = None
with io.open('docker_leash/__init__.py', 'rt', encoding='utf8') as fobj:
    VERSION = re.search(
        r'''__version__\s*=\s*(?P<q>["'])(.*)(?P=q)''',
        fobj.read(),
        re.M,
    ).group(2)

GITHUB_PATH = 'docker-leash/leash-server'

with io.open('README.rst', 'rt', encoding='utf8') as fobj:
    README = fobj.read()
    a, b = README.index('Introduction'), README.index('.. ')
    LONG_DESCRIPTION = README[a:b].lstrip()


setup(
    name='docker-leash',
    version=VERSION,
    author='Mathieu Alorent',
    author_email='docker-leash@kumy.net',
    description='Docker authorization plugin',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    keywords=['docker', 'authz', 'authorization'],
    url='https://github.com/{}'.format(GITHUB_PATH),
    download_url='https://api.github.com/repos/{}/tarball/{}'.format(
        GITHUB_PATH,
        VERSION or ''
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
