Example 1: Everything is allowed (as without the plugin)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You can have all the permissions using this configuration.
This is the same as running docker daemon without this plugin.
Between us, this is not very useful…

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml

.. Note::
   In this case, the `groups.yml` could be empty.
