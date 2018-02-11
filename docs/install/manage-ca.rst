.. _manage-ca-label:

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
