Server Installation (leash)
###########################

The server can be launched from a `virtualenv` or a `docker container`.

Even if it is not mandatory, we recommend to run the service over TLS,
`gunicorn` can do it since version 17.0. Alternativelly, you can use any reverse
proxy you are used to.

Also, `Flask` ship an internal webserver, it should be
avoided on production, just use a dedicated WSGI HTTP Server like `gunicorn` or
`wsgi`.

.. contents:: Table of Contents

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

Next, read :doc:`client-installation` if your planned rules don't rely on
`clients hostname` or `images/containers names` else :doc:`collar-installation`.
