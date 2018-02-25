.. _client-installation-label:

Client Installation (json)
##########################

On `docker daemon`, you can connect to the `leash-server` using a simple
`json`, but this imply that your planned rules don't rely on `clients hostname`
nor `images/containers names`. If that's not the case, then refer to the
:doc:`collar-installation`.

.. toctree::
   :maxdepth: 4

Deploy the json file
====================

The connection to the `leash-server` rely on a simple json file placed in usually
in the `/etc/docker/plugins/` directory.

.. code-block:: json
   :caption: /etc/docker/plugins/leash.json

    {
      "Name": "leash",
      "Addr": "https://docker-leash.kumy.org",
      "TLSConfig": {
        "InsecureSkipVerify": false,
        "CAFile": "/etc/docker/plugins/cacert-root.pem"
      }
    }

Fill the `Addr` field with your `leash-server` url. Point the `CAFile` field
to the path of the CA used to sign `leash-server` webservice.

Even if it's not recommended, you can disable SSL certificate verification by
setting the `InsecureSkipverify` field to `true`.


Activate the plugin
===================

Edit the `docker daemon` configuration and add `authorization-plugins` field to
enable the plugin.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["leash"]
   }

Now restart `dockerd`.

.. code-block:: console
   :caption: restart the `docker` daemon

   $ systemctl restart docker


Next, read :doc:`users-authentication`.
