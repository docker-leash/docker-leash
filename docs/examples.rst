Examples
========

Everything is allowed (as without the plugin)
+++++++++++++++++++++++++++++++++++++++++++++

You can have all the permissions using this configuration.
This is the same as running docker daemon without this plugin.

.. code-block:: yaml
   :caption: policies.yml

   ---
   masteroftheuniverse:
     all:
       Allow:
   ...

.. code-block:: yaml
   :caption: groups.yml

   ---
   all:
     policies:
       - masteroftheuniverse
     members:
       - "*"
   ...

Read only / write
-----------------

Here we want all users to have only the ability to execute read only
commands whereas the administrators will have access the write commands too.

.. code-block:: yaml
   :caption: policies.yml

   ---
   readonly:
     all:
       ReadOnly:

   readwrite:
     all:
       ReadWrite:
   ...

.. code-block:: yaml
   :caption: groups.yml

   ---
   all:
     policies:
       - readonly
     members:
       - "*"

   administrators:
     policies:
       - readwrite
     members:
       - rda
       - mal
   ...

Restrict by container name
--------------------------

Here we want all users to have a limitation by the container name.
All administrators are allowed to manage all containers.

.. code-block:: yaml
   :caption: policies.yml

   ---
   containers_name_must_match_username:
     containers:
       containerNameCheck:
         startwith:
           - "$USER-"

   readwrite:
     all:
       ReadWrite:
   ...

.. code-block:: yaml
   :caption: groups.yml

   ---
   all:
     policies:
       - containers_name_must_match_username
     members:
       - "*"

   administrators:
     policies:
       - readwrite
     members:
       - rda
       - mal
   ...
