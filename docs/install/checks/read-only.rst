.. _read-only-label:

ReadOnly
========

Allow the request if is `read-only`. ie: method of the `docker API` is of type
`GET` or `HEAD`.

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 12

   ---

   - description: Allow only read-only actions.
     hosts:
       - +.*
     default: Deny
     policies:
       - members:
           - all
         rules:
           any:
             ReadOnly:

   ...
