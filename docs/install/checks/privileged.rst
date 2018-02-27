.. _privileged-label:

Privileged
==========

Allow the request if the container don't require `privileged` flag.

Volumes name check is a list or regular expressions.

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 13

   ---

   - description: Allow action only if the container has `privileged` flag off.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - all
         rules:
           containers:
             Privileged:

   ...
