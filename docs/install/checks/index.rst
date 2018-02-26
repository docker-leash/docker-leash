
"Checks" list
-------------

The `checks` are some sort of plugin to `leash-server`.
They permit to verify/filter the access to one or more resources.

+------------------------------+---------------------------------------------+
| check name                   | Description                                 |
+==============================+=============================================+
| :ref:`allow-label`           | Authorize the request inconditionnally      |
+------------------------------+---------------------------------------------+
| :ref:`deny-label`            | Deny the request inconditionnally           |
+------------------------------+---------------------------------------------+
| :ref:`read-only-label`       | Allow only read-only actions                |
+------------------------------+---------------------------------------------+
| :ref:`bind-mount-label`      | Restrict bind mounts                        |
+------------------------------+---------------------------------------------+
| :ref:`container-name-label`  | Restrict by container name                  |
+------------------------------+---------------------------------------------+
| :ref:`image-name-label`      | Restrict image name                         |
+------------------------------+---------------------------------------------+
| :ref:`volume-name-label`     | Restrict volume name                        |
+------------------------------+---------------------------------------------+
| :ref:`privileged-label`      | Check the privileged flag                   |
+------------------------------+---------------------------------------------+
| :ref:`user-label`            | Restrict user                               |
+------------------------------+---------------------------------------------+

.. Note::
   More checks to come.
   See the `related issues in our repository
   <https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Amodule>`__.
