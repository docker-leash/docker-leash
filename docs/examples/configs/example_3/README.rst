Example 3: Restrict by container name
+++++++++++++++++++++++++++++++++++++

Here we want all users from groups `group1` and `group2` to manage only
containers having their name starting with `foo-` or `bar-` or `$USER-`.
Otherwize read-only actions are permitted. All administrators are allowed to
manage all containers. Anonymous and all other users cannot do anything.

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml
