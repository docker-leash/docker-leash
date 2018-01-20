Installation
############

The server can be launched from a `virtualenv` or a `docker container`.

Even if it is not mandatory, we recommend to run the service over TLS,
`gunicorn` can do it since version 17.0. Alternativelly, you can use any reverse
proxy you are used to.

Also, `Flask` ship an internal webserver, it should be
avoided on production, just use a dedicated WSGI HTTP Server like `gunicorn` or
`wsgi`.

.. contents:: Table of Contents

Install the server
==================

The server is the central point of authorization and configuration.
Run it on a server reachable by your clients (docker daemon).
For a better availability, don't hesitate to scale your deployment.

Using virtualenv
++++++++++++++++

.. code-block:: console
   :caption: Install Docker Leash in a `virtualenv`

   $ virtualenv venv
   $ source ./venv/bin/activate
   $ pip install docker-leash
   $ pip install -r requirements.txt

Running the service
-------------------

Using flask internal webserver
''''''''''''''''''''''''''''''

.. code-block:: console
   :caption: Launch Docker Leash using Flask internal server.

   $ export FLASK_APP=docker_leash.leash_server.py
   $ python -m flask run --host 0.0.0.0 --port 80
    * Running on http://[::]:80/

Using gunicorn
''''''''''''''

.. code-block:: console
   :caption: Launch Docker Leash with gunicorn.

   $ gunicorn --workers=5 --bind=[::]:80 --reload \
     docker_leash.leash_server:app

If you choose to support TLS directly with `gunicorn`, just add options
`certfile`, `keyfile`, `ciphers` and change port listen port to `443`:

.. code-block:: console
   :caption: Launch gunicorn with TLS support.

   $ gunicorn --workers=5 --bind=[::]:443 --reload \
     --certfile=/certs/server.crt --keyfile=/certs/server.key \
     --ciphers=TLSv1.2 \
     docker_leash.leash_server:app

Using Docker container
++++++++++++++++++++++

.. Warning::
   Of course, the `docker-leash` server could be deployed as a Docker container,
   but be careful to don't brick yourself by running the container
   on the same host as the one you want to secure.

We publish ready to use container images on Docker Hub,
please have a look at our `docker repository <https://hub.docker.com/r/dockerleash/leash-server/>`_.

Building the image
------------------

You may want to build the image yourself.

.. code-block:: console
   :caption: Build docker image from sources.

   $ git clone https://github.com/docker-leash/leash-server.git
   $ cd leash-server
   $ docker build -t leash-server .

Running the service
-------------------

You can simply launch the service using `docker cli` or `docker-compose`.
Don't forget to mount the configuration over the respective files.

.. code-block:: console
   :caption: Launch `docker-leash` using `docker`.

   $ docker run \
     -d \
     -p 443:443 \
     -v /path/to/your/certs/:/certs:ro \
     -v /path/to/your/conf/groups.yml:/srv/docker-leash/groups.yml:ro \
     -v /path/to/your/conf/policies.yml:/srv/docker-leash/policies.yml:ro \
     --certfile=/certs/server.crt --keyfile=/certs/server.key \
     --ciphers=TLSv1.2 \
     dockerleash/leash-server:latest \
     gunicorn --workers=5 --bind=[::]:443 app.leash_server:app

.. code-block:: yaml
   :caption: docker-compose.yml

   version: '2'

   services:
     leashserver:
       image: dockerleash/leash-server:latest
       command: gunicorn --workers=5 --bind=[::]:443 --chdir=/srv/docker-leash \
         --certfile=/certs/server.crt --keyfile=/certs/server.key \
         --ciphers=TLSv1.2 \
         docker_leash.leash_server:app
       volumes:
         - /path/to/your/certs/:/certs:ro
         - /path/to/your/conf/groups.yml:/srv/docker-leash/groups.yml:ro
         - /path/to/your/conf/policies.yml:/srv/docker-leash/policies.yml:ro
       ports:
         - "443:443"
       restart: always

Alternatively, you can build a child image including your configuration.

.. code-block:: dockerfile
   :caption: Your personnal `Dockerfile`

   FROM dockerleash/leash-server:latest
   COPY configuration/*.yml /srv/docker-leash/
   COPY certs/* /certs/

.. note::
   The current `command` launched from the image doesn't include TLS options,
   and listen by default on port `80`. Indeed, the bind mount of `/certs`, is
   optionnal.

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
       "CAFile": "/etc/pki/CA/certs/ca.used.to.sign.docker-leash.crt"
     }
   }

Replace the `Addr` field with the full url of your `leash server` instance.

If you secured the server part with `TLS` using a self-signed certificate,
declare the `CA` in the `CAFile` field.

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
	   "tlscacert": "/etc/pki/CA/certs/our.company.ca.to.authenticate.users.crt",
	   "tlscert": "/etc/pki/tls/certs/full.name.of.your.host.crt",
	   "tlskey": "/etc/pki/tls/private/full.name.of.your.host.key"
   }

Use your favorite `SSL Certificate` provider to encrypt traffic over the tcp
socket. Set fields `tlscert` and `tlskey` to the path of your files.

The `tlscacert`, is responsible for authenticating your clients certificates.
We recommend to manage your own :abbr:`CA (Certificate Authority)`, see `Manage your CA using EasyRSA`_.

.. Note::
   On Ubuntu: You may encounter error "`unable to configure the Docker daemon with file /etc/docker/daemon.json: the following directives are specified both as a flag and in the configuration file: hosts: (from flag: [fd://], from file: [unix:///var/run/docker.sock 0.0.0.0:2376])`."
   In such case, override systemd script:

      $ systemctl edit docker

      | [Service]
      | ExecStart=
      | ExecStart=/usr/bin/dockerd

By default, access to the docker daemon is restricted by the permissions set on
the unix socket (generally `unix:///var/run/docker.sock`). If your planned
policies don't need to know users identity (only anonymous rules), then you can
skip the TLS configuration.

.. code-block:: json
   :caption: /etc/docker/daemon.json

   {
	   "authorization-plugins": ["leash"],
	   "hosts": ["unix:///var/run/docker.sock"]
   }


Users authentication via TLS
++++++++++++++++++++++++++++

For advanced features, users need to authenticate with the `docker daemon`. The
current way is use `clients certificates`.

`The official docker documentation <https://docs.docker.com/engine/security/https/#create-a-ca-server-and-client-keys-with-openssl>`_
has a nice tutorial on how to manage :abbr:`CA (Certificate Authority)`, `Server` and
`Client` certificates.

Manage your CA using EasyRSA
----------------------------

We choose to use `EasyRSA <https://github.com/OpenVPN/easy-rsa>`_ CLI utility
to build and manage our :abbr:`PKI (Public Key Infrastructure)` CA. Their
`README.quickstart.md <https://github.com/OpenVPN/easy-rsa/blob/v3.0.4/README.quickstart.md>`_
has good informations on basic usage. Please refer to their
`documentation <https://github.com/OpenVPN/easy-rsa/blob/v3.0.4/doc/EasyRSA-Readme.md>`_
for general usage of EasyRSA.

.. Note::
   We are used to encrypt the socket traffic using `CAcert.org <http://cacert.org>`_
   and authenticate our users using our own
   :abbr:`CA (Certificate Authority)` (:abbr:`pki (Public Key Infrastructure)`).
   But you can also use your own managed CA to accomplish both.


EasyRSA PKI initialization
'''''''''''''''''''''''''''

.. code-block:: bash
   :caption: Initialize an EasyRSA PKI.

   # Obtain EasyRSA
   #
   $ wget https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.3/EasyRSA-3.0.3.tgz
   $ tar xf EasyRSA-3.0.3.tgz
   $ cd EasyRSA-3.0.3


   # Configure EasyRSA
   #
   $ cp vars.example vars
   # Edit `vars` file and adapt to your need. You probably need to
   # uncomment EASYRSA_REQ_* directives ;)
   $ vim vars


   # Initialize the pki
   #
   $ ./easyrsa init-pki
   $ ./easyrsa build-ca

   # Copy the CA public key to a central path
   $ cp pki/ca.crt /etc/pki/CA/certs/our.company.ca.to.authenticate.users.crt


   # If you choose to use your managed CA to encrypt the socket,
   # then let's generate a certificate for it. Please replace
   # `full.name.of.your.host` with the value you plan to use
   # for accessing the docker socket (aka DOCKER_HOST envvar).
   #
   $ ./easyrsa build-server-full full.name.of.your.host nopass

   # Place the generated certificates in a know directory and
   # use them in your `/etc/docker/daemon.json` file
   # (`tlskey` / `tlscert`)
   #
   $ cp pki/issued/full.name.of.your.host.crt /etc/pki/tls/certs/full.name.of.your.host.crt
   $ cp pki/private/full.name.of.your.host.key /etc/pki/tls/certs/full.name.of.your.host.key


Generate client certificat for user
'''''''''''''''''''''''''''''''''''

.. code-block:: bash
   :caption: Generate a client certificate for `username1`.


   # Generate a client certificate
   #
   $ ./easyrsa build-client-full username1 nopass

   # Place generated files in user's home directory
   #
   $ mkdir /home/username1/.docker/
   $ install -o username1 -g username1 -m 0444 pki/issued/username1.crt /home/username1/.docker/cert.pem
   $ install -o username1 -g username1 -m 0400 pki/private/username1.key /home/username1/.docker/key.pem
   $ install -o username1 -g username1 -m 0444 pki/ca.crt /home/username1/.docker/ca.pem

   # Check everything is working
   $ docker --tlsverify -H=full.name.of.your.host:2376 version
   # or
   $ DOCKER_HOST=tcp://full.name.of.your.host:2376 DOCKER_TLS_VERIFY=1 docker version
