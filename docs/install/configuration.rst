Configuration
#############

.. contents:: Table of Contents

Configure the rules
===================

The users authorizations are defined on `leash-server` side.
Configurations are stored as a Yaml file.
We have one file to defining groups of users, and one for the rules.
If no matching `docker action` are defined for a specific action, then the default is to **deny** the request.
On `docker action` we can attach some `checks`.
When a request is received, all `checks` are passed over the payload for the `docker action`.
If one of the check fail, then the whole request is refused.
If no `check` fail then the action is authorized.

Policies configuration file format
++++++++++++++++++++++++++++++++++

.. code-block:: yaml

   ---

   openbar:
     containersCreate:
       Allow:
     containersWait:
       Allow:
     containersStart:
       Allow:
     containersAttach:
       Allow:

   personnal:
     containersCreate:
       containerNameCheck:
         startwith:
           - foo
           - bar
     containersWait:
       containerNameCheck:
         startwith:
           - foo
           - bar
     containersStart:
       containerNameCheck:
         startwith:
           - foo
           - bar
     containersAttach:
       containerNameCheck:
         startwith:
           - foo
           - bar

   restricted:
     containersCreate:
       pathCheck:
         - "-/"
         - "+/home/$USER"
         - "+/0"
     containersDelete:
       Deny:

   readonly:
     ping:
       Allow:
     containersList:
       Allow:

   ...

We can break down the sections as follow.
You can define `policy name` should match `policy name` they will be matched in `groups.yml` file.
The `docker action` is a name of an action (see bellow for the list).
The `check name` is the internal name of the check to apply on the command, and `check argument` are the arguments for the check (see bellow for the list).

.. code-block:: yaml

   <policy name>:
     <docker action>:
       <check name>:
         - <check argument 1>
         - <check argument 2>

Docker actions list
-------------------

Docker action names are a mapping to the internal actions from the
`Docker API <https://docs.docker.com/engine/api/version-history/>`_.

+--------------------------------------+-------------------------------------+
| action name                          | API description                     |
+======================================+=====================================+
| containersList                       | List containers                     |
+--------------------------------------+-------------------------------------+
| containersCreate                     | Create containers                   |
+--------------------------------------+-------------------------------------+
| containersInspect                    | Inspect container                   |
+--------------------------------------+-------------------------------------+
| containersListProcess                | List processes running inside       |
|                                      | a container                         |
+--------------------------------------+-------------------------------------+
| containersLogs                       | Get container logs                  |
+--------------------------------------+-------------------------------------+
| containersChanges                    | Get changes on a container’s        |
|                                      | filesystem                          |
+--------------------------------------+-------------------------------------+
| containersExport                     | Export a container                  |
+--------------------------------------+-------------------------------------+
| containersStats                      | Get container stats based on        |
|                                      | resource usage                      |
+--------------------------------------+-------------------------------------+
| containersResizeTTY                  | Resize a container TTY              |
+--------------------------------------+-------------------------------------+
| containersStart                      | Start a container                   |
+--------------------------------------+-------------------------------------+
| containersStop                       | Stop a container                    |
+--------------------------------------+-------------------------------------+
| containersRestart                    | Restart a container                 |
+--------------------------------------+-------------------------------------+
| containersKill                       | Kill a container                    |
+--------------------------------------+-------------------------------------+
| containersUpdate                     | Update a container                  |
+--------------------------------------+-------------------------------------+
| containersRename                     | Rename a container                  |
+--------------------------------------+-------------------------------------+
| containersPause                      | Pause a container                   |
+--------------------------------------+-------------------------------------+
| containersAttach                     | Unpause a container                 |
+--------------------------------------+-------------------------------------+
| containersAttach                     | Attach to a container               |
+--------------------------------------+-------------------------------------+
| containersAttachWebsocket            | Attach to a container via a         |
|                                      | websocket                           |
+--------------------------------------+-------------------------------------+
| containersAttachWebsocket            | Wait for a container                |
+--------------------------------------+-------------------------------------+
| containersRemove                     | Remove a container                  |
+--------------------------------------+-------------------------------------+
| containersGetInfoAboutFiles          | Get information about files         |
|                                      | in a container                      |
+--------------------------------------+-------------------------------------+
| containersGetFilesystemArchive       | Get an archive of a filesystem      |
|                                      | resource in a container             |
+--------------------------------------+-------------------------------------+
| containersExtractArchiveToDirectory  | Extract an archive of files or      |
|                                      | folders to a directory              |
|                                      | in a container                      |
+--------------------------------------+-------------------------------------+
| containersPrune                      | Delete stopped containers           |
+--------------------------------------+-------------------------------------+

.. Note::
   More actions to come.
   See the `related issues on our repository
   <https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Aaction>`__.

Checks list
-----------

The `checks` are some sort of plugin to `leash-server`.
They permit to verify/filter the access to one or more resources.

+------------+---------------+
| check name | Description   |
+============+===============+
| allow      | Just say yes  |
+------------+---------------+
| deny       | Just say no   |
+------------+---------------+

.. Note::
   More checks to come.
   See the `related issues on our repository
   <https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Amodule>`__.

Groups configuration file format
================================

Here is a sample `groups.yml`:

.. code-block:: yaml

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
`policies` and `members` are reserved words.
You can define `group name` to the name of your choice.
`policy name` should match `policy name` from the `policies.yml` file.
Finally, `username` should match the `CN` field from the user `ssl client certificate`.

.. code-block:: yaml

   <group name>:
     policies:
       - <policy name 1>
       - <policy name 2>
     members:
       - <username 1>
       - <username 2>

Examples
========

Everything is possible (as without the plugin)
++++++++++++++++++++++++++++++++++++++++++++++

You can have all permission using this configuration.
This is the same as running docker daemon without  this plugin.

`policies.yml`:

.. code-block:: yaml

   ---
   masteroftheuniverse:
     all:
       Allow:
   ...

`groups.yml`:

.. code-block:: yaml

   ---
   all:
     policies:
       - masteroftheuniverse
     members:
       - "*"
   ...

Read only / write
-----------------

Here we want all users to have only the possibility to execute read only commands whereas the administrators will have access the the write commands.

`policies.yml`:

.. code-block:: yaml

   ---
   readonly:
     all:
       ReadOnly:

   readwrite:
     all:
       ReadWrite:
   ...

`groups.yml`:

.. code-block:: yaml

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

`policies.yml`:

.. code-block:: yaml

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

`groups.yml`:

.. code-block:: yaml

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
