.. _user-label:

User
====

Allow the request if the container will user as `user`.

For references, see the
`docker run documentation <https://docs.docker.com/engine/reference/run/#user>`_.

Volumes name check is a list or regular expressions.

Example usage
=============

.. code-block:: yaml
   :caption: groups.yml
   :emphasize-lines: 13-16

   ---

   - description: Allow action if not running as `root` or running as `$USER` or
                  `someone`.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - all
         rules:
           containers:
             User:
               - "+^$USER$"
               - "+^someone$"
               - "-^root$"
   ...
