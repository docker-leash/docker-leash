docker-leash
############

.. list-table::
   :align: center

   * - Builds
     - .. image:: https://travis-ci.org/docker-leash/leash-server.svg?branch=master
          :target: https://travis-ci.org/docker-leash/leash-server

       .. image:: https://readthedocs.org/projects/docker-leash/badge/
          :target: http://docker-leash.readthedocs.io/en/latest/

       .. image:: https://img.shields.io/docker/build/dockerleash/leash-server.svg
          :target: https://hub.docker.com/r/dockerleash/leash-server/

   * - Tests
     - .. image:: https://codecov.io/gh/docker-leash/leash-server/branch/master/graph/badge.svg
          :target: https://codecov.io/gh/docker-leash/leash-server

       .. image:: https://api.codacy.com/project/badge/grade/444467f3204246318ddc8a1af5af89bc
          :target: https://www.codacy.com/app/docker-leash/leash-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=docker-leash/leash-server&amp;utm_campaign=badge_grade

Introduction
============

A remote AuthZ plugin to enforce granular rules
for a Docker multiuser environment.

Have you ever wanted to restrict users on your system to manage
only certain containers?
Did you ever wanted to restrict which path can be bind mounted?
Did you ever wanted to log every commands run by your users?
Did you ever need to restrict where images can pushed or pulled?
If you though *yes*, then ``docker-leash`` is for you.

Docker Leash is a centralized point for managing authorization
for your Docker daemon.
It is distributed as a web application backed by Flask_
and distributed in a friendly `MIT license`_.

For more information, we encourage you the read the documentation
online `hosted at ReadTheDocs.org <http://docker-leash.readthedocs.io/>`_.

.. Warning::
   This is a work in progress.
   Things are not yet stable and are subject to change without notice.

.. _Flask: http://flask.pocoo.org/

.. _MIT license: ./LICENSE

Contribute
==========

We will be pleased to receive your contributions as `Pull Requests`_
or as `Reported Issues`_.

You may want contribute to add new checks, see the `contribute page`_.

.. _Pull Requests: https://github.com/docker-leash/leash-server/pulls
.. _Reported Issues: https://github.com/docker-leash/leash-server/issues
.. _contribute page: ./CONTRIBUTE
