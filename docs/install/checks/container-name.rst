.. _container-name-label:

ContainerName
=============

Allow the request if the container name respect the rules.

If you wish to use this module then we recommend to
:doc:`install the collar <../collar-installation>` it will enrich `docker API`
requests by replacing `numeric ids` by `human readable` names used in the
`ContainerName` rules.

Containers name check is a list or regular expressions.

Example usage
=============

.. code-block:: yaml
   :caption: policies.yml
   :emphasize-lines: 12-15

   ---

   - description: Allow action only if container names respect the rules.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - all
         rules:
           containers:
             ContainerName:
               - ^foo-
               - ^bar-
               - ^$USER-

   ...
