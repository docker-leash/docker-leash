.. _deny-label:

Deny
====

Deny the request inconditionnally.

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 12

   ---

   - description: Everything is disallowed.
     hosts:
       - +.*
     default: Deny
     policies:
       - members:
           - all
         rules:
           any:
             Deny:

   ...

.. Note::
   This example is a bit silly, as the default rule is `Deny`. It could have been
   written as follow.

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 6

   ---

   - description: Everything is disallowed.
     hosts:
       - +.*
     default: Deny

   ...
