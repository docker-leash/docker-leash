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
   $ pip install -r requirements.txt

Running the service
-------------------

Using flask internal webserver
''''''''''''''''''''''''''''''

.. code-block:: console

   $ export FLASK_APP=app.leash_server.py
   $ python -m flask run --host 127.0.0.1 --port 65000
    * Running on http://127.0.0.1:65000/

Using gunicorn
''''''''''''''

.. code-block:: console

   $ gunicorn --workers=5 --bind=0.0.0.0:65000 --reload \
     app.leash_server:app

Using Docker container
++++++++++++++++++++++

Of course, the `docker-leash` server could be deployed as a Docker container,
but be careful to don't brick yourself by running the container
on the same host as the one you want to secure.

We publish ready to use container images on Docker Hub,
please have at our `docker repository <https://hub.docker.com/r/dockerleash/leash-server/>`_.

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
Don't forget to mount the configuration in the `/conf` directory.

.. code-block:: console

   $ docker run \
     -d \
     -p 80:80 \
     -v /path/to/your/conf:/configuration:ro \
     dockerleash/leash-server:latest \
     gunicorn --workers=5 --bind=0.0.0.0:80 app.leash_server:app

.. code-block:: yaml
   :caption: docker-compose.yml

   version: '2'

   services:
     leashserver:
       image: dockerleash/leash-server:latest
       volumes:
         - /path/to/your/conf:/configuration:ro
       ports:
         - "80:80"
       restart: always

Alternatively, you can build a child image including your configuration.

.. code-block:: dockerfile

   FROM dockerleash/leash-server:latest
   COPY configuration /configuration

Install local docker plugin
===========================

Create your docker plugin
+++++++++++++++++++++++++

As the configuration depends on your local configuration, we don't provide a `docker plugin` directly from the docker hub.
However, you could build your personalized plugin by editing files from directory `plugin` according to your environment.
Then build and push the plugin to your local registry.

.. code-block:: console

   $ cd plugin
   $ vim leash-client.json
   $ docker plugin create leash-client .
   $ docker plugin push leash-client

Install your docker plugin
++++++++++++++++++++++++++

Now that you have your JSON file deployed, you can install it on your docker hosts:

.. code-block:: console

   $ docker plugin install leash-client
   $ docker plugin ls

Authenticating to the daemon
============================

Please note that this plugin do **authorization** and **not authentication**.
You don't have many choices on the method to authenticate from the `docker client` to the `docker daemon`.
The current - and only - method is to use SSL client certificates.
We redirect you to the `official docker documentation <https://docs.docker.com/engine/security/https/>`_.
