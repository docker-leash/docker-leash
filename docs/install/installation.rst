Installation
############

The server can be launched from a `virtualenv` or a `docker container`.
Even if it is not mandatory, we recommend to run the service over TLS, so use any reverse proxy you are used to.
Also, `Flask` ship an internal webserver, it should be avoided on production, just use a dedicated WSGI HTTP Server like `gunicorn` or `wsgi`.

.. contents:: Table of Contents

Install the server
==================

The server is the central point of authorization and configuration.
Run it on a server reachable by your clients (docker daemon).
For a better availability, don't hesitate to scale your deployment.

Using virtualenv
++++++++++++++++

.. code-block:: console

   $ virtualenv venv
   $ source ./venv/bin/activate
   $ pip install docker-leash
   $ pip install -r requirements.txt

Running the service
-------------------

Using flask internal webserver
''''''''''''''''''''''''''''''

.. code-block:: console

   $ export FLASK_APP=docker_leash.leash_server.py
   $ python -m flask run --host 0.0.0.0 --port 80
    * Running on http://0.0.0.0:80/

Using gunicorn
''''''''''''''

.. code-block:: console

   $ gunicorn --workers=5 --bind=0.0.0.0:80 --reload \
     docker_leash.leash_server:app

Using Docker container
++++++++++++++++++++++

Of course, the `docker-leash` server could be deployed as a Docker container,
but be careful to don't brick yourself by running the container
on the same host as the one you want to secure.

We publish ready to use container images on Docker Hub,
please have a look at our `docker repository <https://hub.docker.com/r/dockerleash/leash-server/>`_.

Building the image
------------------

You may want to build the image yourself.

.. code-block:: console

   $ git clone https://github.com/docker-leash/leash-server.git
   $ cd leash-server
   $ docker build -t leash-server .

Running the service
-------------------

You can simply launch the service using `docker cli` or `docker-compose`.
Don't forget to mount the configuration over the respective files.

.. code-block:: console

   $ docker run \
     -d \
     -p 80:80 \
     -v /path/to/your/conf/groups.yml:/srv/docker-leash/groups.yml:ro \
     -v /path/to/your/conf/policies.yml:/srv/docker-leash/policies.yml:ro \
     dockerleash/leash-server:latest \
     gunicorn --workers=5 --bind=0.0.0.0:80 app.leash_server:app

.. code-block:: yaml
   :caption: docker-compose.yml

   version: '2'

   services:
     leashserver:
       image: dockerleash/leash-server:latest
       volumes:
         - /path/to/your/conf/groups.yml:/srv/docker-leash/groups.yml:ro
         - /path/to/your/conf/policies.yml:/srv/docker-leash/policies.yml:ro
       ports:
         - "80:80"
       restart: always

Alternatively, you can build a child image including your configuration.

.. code-block:: dockerfile

   FROM dockerleash/leash-server:latest
   COPY configuration/*.yml /srv/docker-leash/

Configure docker leash client (Your docker daemon)
==================================================

On `docker daemon` side (the client in our case), the plugin configuration
consist of a simple `.json` file. Copy our sample file located in `plugin/leash.json`
to `/etc/docker/plugins/leash.json` or `/usr/lib/docker/plugins/leash.json`.

Configure the plugin
++++++++++++++++++++

The `leash.json` file need to be configured according to your local environment.

.. code-block:: json
   :caption: /etc/docker/plugins/leash.json

   {
     "Name": "leash",
     "Addr": "https://leash-server.organization.yours",
     "TLSConfig": {
       "InsecureSkipVerify": false,
       "CAFile": "/etc/pki/CA/certs/company.crt"
     }
   }

Replace the `Addr` field with the full url of your `leash server` instance.
If you secured the server part with `TLS`, declare the `CA` in the `CAFile`
field.

.. Note::
   The fields `CertFile` and `KeyFile` are present in the
   `docker documentation <https://docs.docker.com/engine/extend/plugin_api/#json-specification>`_,
   but unfortunately they are not documented...

Even if - on a security point of view - this is not recommended, you can also
choose to not verify the authenticity of the connection, by setting field
`InsecureSkipVerify` to `true`.

.. code-block:: json
   :caption: /etc/docker/plugins/leash.json

   {
     "Name": "leash",
     "Addr": "https://leash-server.organization.yours",
     "TLSConfig": {
       "InsecureSkipVerify": true,
     }
   }

Load the plugin on docker daemon start
++++++++++++++++++++++++++++++++++++++

The `docker daemon` need to start the plugin on boot. You have many
possibilities depending on how you launch the docker daemon (ex: `systemd`), but
the simplest way seems to configure it directly in the `/etc/docker/daemon.json`.

Add the `authorization-plugins` and the `tcp socket` (`"0.0.0.0:2376"`) entry as:

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["leash"],
	   "hosts": ["unix:///var/run/docker.sock", "0.0.0.0:2376"],
	   "tls": true,
	   "tlsverify": true,
	   "tlscacert": "/etc/pki/CA/certs/company.crt",
	   "tlscert": "/etc/pki/tls/certs/dockerhost.crt",
	   "tlskey": "/etc/pki/tls/private/dockerhost.key"
   }

We will generate `tlscacert`, `tlscert` and `tlskey` later.

By default, access to the docker daemon is restricted by the permissions set on the unix
socket (generally `unix:///var/run/docker.sock`). If your planned policies don't need to
know users identity (only anonymous rules), then you can skip the TLS configuration.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["leash"],
	   "hosts": ["unix:///var/run/docker.sock"]
   }


Users authentication via TLS
++++++++++++++++++++++++++++

For advanced features, users need to authenticate with the `docker daemon`. The current way is
use `clients certificates`.

`The official docker documentation <https://docs.docker.com/engine/security/https/#create-a-ca-server-and-client-keys-with-openssl>`_
has a nice tutorial to manage a `Certificate Authority`, `Server` and `Client` certificates. We'll
try to provide explanations to manage your CA using EasyRSA.

Manage your CA using EasyRSA
++++++++++++++++++++++++++++

TBD
