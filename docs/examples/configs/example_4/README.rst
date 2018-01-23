Example 4: Server are manageable only by admins
+++++++++++++++++++++++++++++++++++++++++++++++

Here we want to give access to the servers only by admins. All other hosts
are fully accessible by connected users from group but not from admins.
Anonymous or other users cannot do anything.

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml
