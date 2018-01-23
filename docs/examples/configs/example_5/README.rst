Example 5: Server are manageable by admins, workstations by users
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Here we want to give full access to the admins. Workstations are
are restricted to authenticated users, bind mounts are limited to `/home/$USER/`
and can only manage `containers` and `images`. All other actions are read-only.
Unauthenticated users cannot do anything on workstations.
All other hosts are read-only even for admins.

.. literalinclude:: policies.yml
   :caption: policies.yml
   :language: yaml

.. literalinclude:: groups.yml
   :caption: groups.yml
   :language: yaml
