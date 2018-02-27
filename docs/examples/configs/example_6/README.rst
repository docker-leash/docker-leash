.. _example6-label:

Example 6: Restrict by run as user name
+++++++++++++++++++++++++++++++++++++++

Here we want the containers to be running as default image `run as` user.
If the user want to override the `run as` user, it is only allowed to `run as`
*his* username or `nobody`.

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml
   :emphasize-lines: 12-14

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml
