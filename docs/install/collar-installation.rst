.. _collar-installation-label:

Collar Installation (client)
############################

On `docker daemon` side, deploy the `docker collar plugin`. The `collar-client`
will enrich requests from the `docker daemon` with `clients hostname`. It will
also try to translate `images` or `containers` `ids` to `human readable names`.
Such conversion are necessary if your planned rules rely on
`images/containers names`. If that's not the case, then refer to the
:doc:`client-installation`.

.. toctree::
   :maxdepth: 4

Build the plugin yourself
=========================

The plugin construction is managed using a `makefile`.

.. code-block:: console
   :caption: building the client image

   $ make rootfs
   $ make create

Installing from registry
========================

We provide prebuilt `docker plugin image` directly available on the
`docker hub <https://hub.docker.com/r/dockerleash/leash-client/>`_.

.. code-block:: console
   :caption: building the client image

   $ docker plugin install dockerleash/leash-client

Configure the plugin
====================

The `collar` need to be configured according to your local environment.

.. Note::
   Plugin need to be disabled to be configured.

Variables:

* LEASH_URL mandatory
* LEASH_CA_CERT /certs/ca.pem
* LEASH_CONNECT_TIMEOUT 10

* DOCKER_CA_CERT /certs/ca.pem
* DOCKER_CERT_FILE /certs/cert.pem
* DOCKER_KEY_FILE /certs/key.pem
* DOCKER_URL https://127.0.0.1:2376
* DOCKER_CONNECT_TIMEOUT 10

* DEBUG default false
* ALLOW_PING default true
* ALLOW_READONLY default false

* SENTRY_DSN default None

Mounts:

* certs /certs/ /etc/docker/plugins/collar.d/

.. code-block:: console
   :caption: Define leash server url

   docker plugin dockerleash/collar:0.1 LEASH_URL=https://your-leash-server


Load the plugin on docker daemon start
======================================

The `docker daemon` need to start the plugin on boot.

.. code-block:: console
   :caption: Enable the collar

   docker plugin enable dockerleash/collar:0.1


Activate the collar
===================

Edit the `docker daemon` configuration.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["dockerleash/collar:0.1"]
   }


Next, read :doc:`users-authentication`.
