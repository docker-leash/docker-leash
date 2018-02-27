.. _bind-mount-label:

BindMount
=========

Authorize the request only if the bind mount option doesn't run over the defined
rules.

Checks are recursive. Every paths not explicitly defined are disallowed. A path
not terminated by a `/` will be considered as starting blob (`/foo*`).

Path starting with `+` represent an allowed path, hence, path starting with `-`
will be disallowed. The special key `$USER` will be replaced by the current
connected user. You can escape the `$` sign by preceding it by a `\` ("\$USER")
to use `$USER` as a litteral.

`BindMount` are on evaluated only if the action include binded paths. That's the
case for:

* :ref:`containers-create-label`

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 12-16

   ---

   - description: Allow everything if bind mounts are validated.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - users
         rules:
           any:
             BindMount:
               - "-/"
               - "+/home/$USER/"
               - "+/0/"
               - "-/mnt/something-"

   ...
