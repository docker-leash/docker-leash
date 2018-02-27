.. _allow-label:

Allow
=====

Authorize the request inconditionnally.

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 12

   ---

   - description: Everything is allowed.
     hosts:
       - +.*
     default: Deny
     policies:
       - members:
           - administrators
         rules:
           any:
             Allow:

   ...
