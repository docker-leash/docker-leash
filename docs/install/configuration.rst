Configuration
#############

.. contents:: Table of Contents

Configure the rules
===================

The users authorizations are defined on `leash-server` side.

Configurations are stored as a YAML file.
We have one file to define `groups of users`, and one for the `rules`.

The `rules` permit to attach `checks` on `docker action`.

.. Important::
   If no matching `docker action` is defined for a specific action, then the default is to **deny** the request.

Policies configuration file format
++++++++++++++++++++++++++++++++++

Example configuration file:

.. code-block:: yaml
   :caption: policies.yml

   ---

   openbar:
     containers:
       Allow:

   developper:
     containers:
       ContainerName:
         - "^foo-.*"
         - "^$USER-.*"
       BindMount:
         - "-/"
         - "+/home/$USER"
         - "+/0"
     containersDelete:
       Deny:

   public:
     readonly:
       Allow:

   ...

We can break down the sections as follow.

.. code-block:: yaml

   <policy name>:
     <docker action>:
       <check name>:
         - <check argument 1>
         - <check argument 2>

"Docker actions" list
---------------------

As the list is quite long, please see the `dedicated page <docker-actions-list.html>`_.

"Checks" list
-------------

The `checks` are some sort of plugin to `leash-server`.
They permit to verify/filter the access to one or more resources.

+------------+---------------------------------------------+
| check name | Description                                 |
+============+=============================================+
| Allow      | Just say yes                                |
+------------+---------------------------------------------+
| Deny       | Just say no                                 |
+------------+---------------------------------------------+
| BindMount  | Validate bind mounts                        |
+------------+---------------------------------------------+

.. Note::
   More checks to come.
   See the `related issues in our repository
   <https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Amodule>`__.

Groups configuration file format
================================

Here is a groups policies configuration sample:

.. code-block:: yaml
   :caption: groups.yml

   ---

   admins:
     policies:
       - openbar
     members:
       - rda
       - mal

   developpers:
     policies:
       - restricted
       - personnal
     members:
       - jre

   all:
     policies:
       - readonly
     members:
       - "*"

   ...

We can break down the sections as follow.

.. code-block:: yaml

   <group name>:
     policies:
       - <policy name 1>
       - <policy name 2>
     members:
       - <username 1>
       - <username 2>
