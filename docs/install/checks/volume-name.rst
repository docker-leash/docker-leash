.. _volume-name-label:

VolumeName
==========

Allow the request if the volumes name respect the rules.

Volumes name check is a list or regular expressions.

Example usage
=============

.. code-block:: yaml
   :caption: groups.yml
   :emphasize-lines: 12-15

   ---

   - description: Allow action only if volumes names respect the rules.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - all
         rules:
           containers:
             VolumesName:
               - ^foo-
               - ^bar-
               - ^$USER-

   ...
