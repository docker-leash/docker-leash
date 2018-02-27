.. _user-label:

User
====

Allow the request if the container will `run as` specified user.

Volumes name check is a list of regular expressions. If one rule is valid, then
the request is validated.

Related documentation
=====================

* `docker run documentation <https://docs.docker.com/engine/reference/run/#user>`_

Examples
========

:ref:`example6-label`

.. literalinclude:: ../../examples/configs/example_6/policies.yml
   :caption: policies.yml
   :language: yaml
   :emphasize-lines: 12-14
