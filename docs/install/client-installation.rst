.. _client-installation-label:

Client Installation (collar)
############################

On `docker daemon` side, deploy the `docker collar plugin`.

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

The `colar` need to be configured according to your local environment.

.. Note::
   Plugin need to be disabled to be configured.

Variables:

* LEASH_URL mandatory
* LEASH_CA_CERT /certs/ca.pem
* LEASH_CONNECT_TIMEOUT 10

* DOCKER_CA_CERT /certs/ca.pem
* DOCKER_KEY_FILE /certs/key.pem
* DOCKER_URL https://127.0.0.1:2376
* DOCKER_CONNECT_TIMEOUT 10

* DEBUG default false

Mounts:

* certs /certs/ /etc/docker/plugins/collar.d/

.. code-block:: console
   :caption: Define leash server url

   docker plugin collar:next LEASH_URL=https://your-leash-server


Load the plugin on docker daemon start
======================================

The `docker daemon` need to start the plugin on boot.

.. code-block:: console
   :caption: Enable the collar

   docker plugin enable collar:next


Activate the collar
===================

Edit the `docker daemon` configuration.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["collar:next"]
   }


User authentication
===================

By default, access to the docker daemon is restricted by the permissions set on
the unix socket (generally `unix:///var/run/docker.sock`). If your planned
policies don't need to know users identity (only anonymous rules), then you can
skip jump to `Need Authentication`_ section.

Anonymous is sufficient
=======================

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
     "authorization-plugins": ["leash"],
     "hosts": ["unix:///var/run/docker.sock"]
   }


Need Authentication
===================

If your planned rules rely on user authentication, then the `docker daemon` need
to have TLS authentication enabled.

.. Note::
   It is only possible to authenticate using SSL certificate only when using TCP
   socket. When connecting to unix socket, users will be threated as anonymous.

You have many possibilities depending on how you launch the docker daemon
(ex: `systemd`, `upstart`…), but the simplest way seems to configure it directly in the
`/etc/docker/daemon.json`.

Add the `tcp socket` (`"0.0.0.0:2376"`) to the `daemon.json` file.

Use your favorite `SSL Certificate` provider to secure the traffic over the tcp
socket. Set fields `tlscert` and `tlskey` to the path of your files.

The `tlscacert`, is responsible for authenticating your clients certificates.
We recommend to manage your own :abbr:`CA (Certificate Authority)`, see `Users authentication via TLS`_.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["collar:next"],
	   "hosts": ["unix:///var/run/docker.sock", "0.0.0.0:2376"],
	   "tls": true,
	   "tlsverify": true,
	   "tlscacert": "/etc/pki/CA/certs/our.company.ca.to.authenticate.users.crt",
	   "tlscert": "/etc/pki/tls/certs/full.name.of.your.host.crt",
	   "tlskey": "/etc/pki/tls/private/full.name.of.your.host.key"
   }

.. Note::
   On Ubuntu: You may encounter error "`unable to configure the Docker daemon
   with file /etc/docker/daemon.json: the following directives are specified both
   as a flag and in the configuration file: hosts: (from flag: [fd://],
   from file: [unix:///var/run/docker.sock 0.0.0.0:2376])`."
   In such case, override systemd script:

      $ systemctl edit docker

      | [Service]
      | ExecStart=
      | ExecStart=/usr/bin/dockerd


Users authentication via TLS
============================

For advanced features, users need to authenticate with the `docker daemon`. The
current way is use `clients certificates`.

`The official docker documentation <https://docs.docker.com/engine/security/https/#create-a-ca-server-and-client-keys-with-openssl>`_
has a nice tutorial on how to manage :abbr:`CA (Certificate Authority)`, `Server` and
`Client` certificates.

We also provide informations to :doc:`manage-ca`.
