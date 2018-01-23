Example 2: Read only / write
++++++++++++++++++++++++++++

Here we want all users to have only the ability to execute read only
commands whereas the administrators will have access the write commands too.
Anonymous users cannot do anything.

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml
