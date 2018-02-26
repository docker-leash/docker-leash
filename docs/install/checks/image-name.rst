.. _image-name-label:

ImageName
=========

Allow the request if the image name respect the rules.

Images name check is a list or regular expressions.

Example usage
=============

.. code-block:: yaml
   :caption: groups.yml
   :emphasize-lines: 12-15

   ---

   - description: Allow action only if images names respect the rules.
     hosts:
       - +.*
     default: Allow
     policies:
       - members:
           - all
         rules:
           containers:
             ImageName:
               - ^foo-
               - ^bar-
               - ^$USER-

   ...
