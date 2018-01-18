.. _docker-actions-list:

Docker actions list
###################

Docker action names are a mapping to the internal actions from the
`Docker API <https://docs.docker.com/engine/api/version-history/>`__.

Containers actions
++++++++++++++++++

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
