#!/usr/bin/env python

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

with io.open('README.rst', 'rt', encoding='utf8') as fobj:
    README = fobj.read()
    a, b = README.index('Introduction'), README.index('.. ')
    long_description = README[a:b].lstrip()


setup(
    name='docker-leash',
    version=version,
    author='Mathieu Alorent',
    author_email='docker-leash@kumy.net',
    description='Docker authorization plugin',
    long_description=long_description,
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
