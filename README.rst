docker-leash
############

|codecov|_ |travis|_ |codacy|_ |rtd|_

A remote AuthZ plugin to enforce granular rules
for a Docker multiuser environment.

Have you ever wanted to restrict users on your system to manage
only certain containers?
Did you ever wanted to restrict witch path can be bind mounted?
Did you ever wanted to log every commands run by your users?
Did you ever need to restrict where images can pushed or pulled?
If you though *yes*, then ``docker-leash`` is for you.

Docker Leash is a centralized point for managing authorization
for your Docker daemon.
It is distributed as a web application backed by Flask_
and distributed in a friendly `MIT license`_.

For more information, we encourage you the read the documentation,
either `locally in this repository <./docs/>`_,
or `hosted at ReadTheDocs.org <http://docker-leash.readthedocs.io/>`_.

.. Warning::
   This is a work in progress.
   Things are not yet stable and are subject to change without notice.

.. |codecov| image:: https://codecov.io/gh/docker-leash/leash-server/branch/master/graph/badge.svg
.. _codecov: https://codecov.io/gh/docker-leash/leash-server

.. |travis| image:: https://travis-ci.org/docker-leash/leash-server.svg?branch=master
.. _travis: https://travis-ci.org/docker-leash/leash-server

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/444467f3204246318ddc8a1af5af89bc
.. _codacy: https://www.codacy.com/app/docker-leash/leash-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=docker-leash/leash-server&amp;utm_campaign=Badge_Grade

.. |rtd| image:: https://readthedocs.org/projects/docker-leash/badge/?version=latest
.. _rtd: http://docker-leash.readthedocs.io/en/latest/?badge=latest

.. _Flask: http://flask.pocoo.org/

.. _MIT license: ./LICENSE

Contribute
==========

We will be pleased to receive your contribution as `Pull Requests`_ or as `Reported Issues`_.

You may want contribute to add new checks, see the `contribute page`_.

.. _Pull Requests: https://github.com/docker-leash/leash-server/pulls
.. _Reported Issues: https://github.com/docker-leash/leash-server/issues
.. _contribute page: ./CONTRIBUTE
