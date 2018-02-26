
Configuration
#############

The users authorizations are defined on `leash-server` side.

Configurations are stored as a YAML file.
We have one file to define `groups of users`, and one for the `policies`.

The `policies` permit to attach `checks` on `docker action`.

Policies configuration file format
==================================

Example configuration file:

.. code-block:: yaml
   :caption: policies.yml

   ---

   - description: Servers are fully accessible to Admins.
                  Monitoring group can only list containers.
                  Default policy is Deny.
     hosts:
       - +^srv\d\d.*
     default: Deny
     policies:
       - members:
           - admins
         rules:
           any:
             Allow:

       - members:
           - monitoring
         rules:
           containersList:
             Allow:


   - description: Users have access to containers and images starting
                  by their name.
                  Admin have full access to the host.
                  Default policy is ReadOnly.
     hosts:
       - +^wks\d\d.*
     default: ReadOnly
     policies:
       - members:
           - admins
         rules:
           any:
             Allow:

       - members:
           - users
         rules:
           containersLogs:
             ContainerName:
               - ^bar-
               - ^foo-
               - ^$USER-
           containers:
             ContainerName:
               - ^foo-
               - ^$USER-
             BindMounts:
               - -/
               - +/home/$USER
               - +/0


   - description: For all other hosts,
                  Admin have full access to the host.
                  Deny access to Anonymous users.
                  Default policy is ReadOnly.
     hosts:
       - +.*
     default: ReadOnly
     policies:
       - members:
           - admins
         rules:
           any:
             Allow:
       - members:
           - Anonymous
         rules:
           any:
             Deny:

   ...

We can break down the sections as follow.

.. code-block:: yaml
   :caption: General file format

   - description: <Optionnal: Human description of the ruleset>
     hosts:
       - <server name regexp>
       - ...
     default: <Default action if no rule match> (Deny, Allow, ReadOnly)
     policies:
       - members:
           - <group name>
           - ...
         rules:
           <action 1>:
             <check>:
           <action 2>:
             <check>:
               - <arg1>
               - <arg2>
               - ...
           <action 3>:
             <check>:
               <arg1>: value
               <arg1>: value
               ...: ...
       - ...:
           - <group name>
           - ...
         rules:
           ...:

"Docker actions" list
---------------------

As the list is quite long, please refer to the :doc:`actions/index` page.

.. include:: checks/index.rst

Groups configuration file format
================================

Here is a groups policies configuration sample:

.. code-block:: yaml
   :caption: groups.yml

   ---

   admins:
     - rda
     - mal

   users:
     - jre
     - lgh
     - dga
     - ore
     - pyr

   monitoring:
     - xymon_1
     - xymon_2

   anonymous:
     - Anonymous

   all:
     - "*"

   ...

We can break down the sections as follow.

.. code-block:: yaml

   <group name>:
     - <username 1>
     - <username 2>

.. Note::
   The `Anonymous` username is a reserved word. It permit to define rules
   explicitly for non connected users.


You're done! If you need, you can now discover some :doc:`../examples`.
