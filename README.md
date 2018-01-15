[![codecov](https://codecov.io/gh/docker-leash/leash-server/branch/master/graph/badge.svg)](https://codecov.io/gh/docker-leash/leash-server)
[![Build Status](https://travis-ci.org/docker-leash/leash-server.svg?branch=master)](https://travis-ci.org/docker-leash/leash-server)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/444467f3204246318ddc8a1af5af89bc)](https://www.codacy.com/app/docker-leash/leash-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=docker-leash/leash-server&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/docker-leash/badge/?version=latest)](http://docker-leash.readthedocs.io/en/latest/?badge=latest)

# docker-leash
A remote AuthZ plugin to enforce granular rules for a Docker multiuser environment.

Have you ever wanted to restrict users on your system to manage only certain containers? Did you ever wanted to restrict witch path can be bind mounted? Did you ever wanted to log every commands run by your users? Did you ever need to restrict where images can pushed or pulled? If 'yes', then `docker-leash` is for you.

Docker Leash is a centralized point for managing authorization for your docker daemon. It is distributed as a web application backed by `Flask`.

**Warning: This is still a work in progress. Things are not yet stable and are subject to change without notice.**

* [Installation](#installation)
  * [Install the server](#install-the-server)
    * [Using virtualenv](#using-virtualenv)
      * [Running the service](#running-the-service)
        * [Using flask internal webserver](#using-flask-internal-webserver)
        * [Using gunicorn](#using-gunicorn)
    * [Using Docker container](#using-docker-container)
      * [Building the image](#building-the-image)
      * [Running the service](#running-the-service)
  * [Install local docker plugin](#install-local-docker-plugin)
    * [Create your docker plugin](#create-your-docker-plugin)
    * [Install your docker plugin](#install-your-docker-plugin)
  * [Authenticating to the daemon](#authenticating-to-the-daemon)
* [Configure the rules](#configure-the-rules)
  * [Policies configuration file format](#policies-configuration-file-format)
    * [Docker actions list](#docker-actions-list)
    * [Checks list](#checks-list)
  * [Groups configuration file format](#groups-configuration-file-format)
  * [Examples](#examples)
    * [Everything is possible (as without the plugin)](#everything-is-possible-as-without-the-plugin)
    * [Read only / write](#read-only--write)
    * [Restrict by container name](#restrict-by-container-name)
* [Contribute](#contribute)

# Installation
The server could be launched from a `virtualenv` or a `docker container`. Even if it is not mandatory, we recommend to run the service over TLS, so use any reverse proxy you are used to. Also, `Flask` ship an internal webserver, it should be avoided on production, just use a dedicated WSGI HTTP Server like `gunicorn` or `wsgi`.

## Install the server
The server is the central point of authorization and configuration. Run it on a server reachable by your clients (docker daemon). For a better availability, don't hesitate to scale your deployment.

### Using virtualenv
```shell
$ virtualenv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

#### Running the service
##### Using flask internal webserver
```shell
$ export FLASK_APP=app.leash_server.py
$ python -m flask run --host 127.0.0.1 --port 65000
 * Running on http://127.0.0.1:65000/
```

##### Using gunicorn
```shell
$ gunicorn --workers=5 --bind=0.0.0.0:65000 --reload app.leash_server:app
```

### Using Docker container
Of course, the `docker-leash` server could be deployed as a Docker container, but be careful to don't brick yourself by running the container on the same host as the one you want to secure.

We publish ready to use container images on Docker Hub, please have at our [docker repository](https://hub.docker.com/r/dockerleash/leash-server/).

#### Building the image
You may want to build the image yourself.

```shell
$ git clone https://github.com/docker-leash/leash-server.git
$ cd leash-server
$ docker build -t leash-server .
```

#### Running the service
You can simply launch the service using `docker cli` or `docker-compose`. Don't forget to mount the configuration in the `/conf` directory.
```shell
$ docker run \
  -d \
  -p 80:80 \
  -v /path/to/your/conf:/configuration:ro \
  dockerleash/leash-server:latest \
  gunicorn --workers=5 --bind=0.0.0.0:80 app.leash_server:app
```

```
version: '2'

services:
  leashserver:
    image: dockerleash/leash-server:latest
    volumes:
      - /path/to/your/conf:/configuration:ro
    ports:
      - "80:80"
    restart: always

```

Alternatively, you can build a child image including your configuration.

```Dockerfile
FROM dockerleash/leash-server:latest
COPY configuration /configuration
```

## Install local docker plugin
### Create your docker plugin
As the configuration depends on your local configuration, we don't provide a `docker plugin` directly from the docker hub. However, you could build your personalized plugin by editing files from directory `plugin` according to your environment. Then build and push the plugin to your local registry.

```shell
$ cd plugin
$ vim leash-client.json
$ docker plugin create leash-client .
$ docker plugin push leash-client
```

### Install your docker plugin
Now that you have your json file deployed, you can install it on your docker hosts:
```
$ docker plugin install leash-client
$ docker plugin ls
```

## Authenticating to the daemon
Please note that this plugin do **authorization** and **not authentication**. You don't have many choices on the method to authenticate from the `docker client` to the `docker daemon`. The current - and only - method is to use SSL client certificates. We gently redirect you to the [official docker documentation](https://docs.docker.com/engine/security/https/)


# Configure the rules
The users authorizations are defined on `leash-server` side. Configurations are stored as a Yaml file. We have one file to defining groups of users, and one for the rules.
If no matching `docker action` are defined for a specific action, then the default is to **deny** the request.
On `docker action` we can attach some `checks`. When a request is received, all `checks` are passed over the payload for the `docker action`.
If one of the check fail, then the whole request is refused. If no `check` fail then the action is authorized.

## Policies configuration file format

```
---

openbar:
  containersCreate:
    Allow:
  containersWait:
    Allow:
  containersStart:
    Allow:
  containersAttach:
    Allow:

personnal:
  containersCreate:
    containerNameCheck:
      startwith:
        - foo
        - bar
  containersWait:
    containerNameCheck:
      startwith:
        - foo
        - bar
  containersStart:
    containerNameCheck:
      startwith:
        - foo
        - bar
  containersAttach:
    containerNameCheck:
      startwith:
        - foo
        - bar

restricted:
  containersCreate:
    pathCheck:
      - "-/"
      - "+/home/$USER"
      - "+/0"
  containersDelete:
    Deny:

readonly:
  ping:
    Allow:
  containersList:
    Allow:

...
```
We can break down the sections as follow. You can define `policy name` should match `policy name` they will be matched in `groups.yml` file. The `docker action` is a name of an action (see bellow for the list). The `check name` is the internal name of the check to apply on the command, and `check argument` are the arguments for the check (see bellow for the list).

```
<policy name>:
  <docker action>:
    <check name>:
      - <check argument 1>
      - <check argument 2>
```

### Docker actions list
Docker action names are a mapping to the internal actions from the [docker api](https://docs.docker.com/engine/api/version-history/).

action name | API description
-----------|---------------
containersList | List containers
containersCreate | Create containers
containersInspect | Inspect container
containersListProcess | List processes running inside a container
containersLogs | Get container logs
containersChanges | Get changes on a container’s filesystem
containersExport | Export a container
containersStats | Get container stats based on resource usage
containersResizeTTY | Resize a container TTY
containersStart | Start a container
containersStop | Stop a container
containersRestart | Restart a container
containersKill | Kill a container
containersUpdate | Update a container
containersRename | Rename a container
containersPause | Pause a container
containersAttach | Unpause a container
containersAttach | Attach to a container
containersAttachWebsocket | Attach to a container via a websocket
containersAttachWebsocket | Wait for a container
containersRemove | Remove a container
containersGetInfoAboutFiles | Get information about files in a container
containersGetFilesystemArchive | Get an archive of a filesystem resource in a container
containersExtractArchiveToDirectory | Extract an archive of files or folders to a directory in a container
containersPrune | Delete stopped containers

Note: More actions to come. See the issues on our [repository](https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Aaction).

### Checks list
The `checks` are some sort of plugin to `leash-server`. They permit to verify/filter the access to one or more resources.

check name | Description
-----------|---------------
allow | Just say yes
deny | Just say no

Note: More checks to come. See the issues on our [repository](https://github.com/docker-leash/leash-server/issues?q=is%3Aopen+is%3Aissue+label%3Amodule).

## Groups configuration file format
Here is a sample `groups.yml` file.
```
---

admins:
  policies:
    - openbar
  members:
    - rda
    - mal

developpers:
  policies:
    - restricted
    - personnal
  members:
    - jre

all:
  policies:
    - readonly
  members:
    - "*"

...
```

We can break down the sections as follow. `policies` and `members` are reserved words. You can define `group name` to the name of your choice. `policy name` should match `policy name` from the `policies.yml` file. Finally, `username` should match the `CN` field from the user `ssl client certificate`.

```
<group name>:
  policies:
    - <policy name 1>
    - <policy name 2>
  members:
    - <username 1>
    - <username 2>
```

## Examples
### Everything is possible (as without the plugin)
You can have all permission using this configuration. This is the same as running docker daemon without  this plugin.

`policies.yml`
```yml
---
masteroftheuniverse:
  all:
    Allow:
...
```

`groups.yml`
```yml
---
all:
  policies:
    - masteroftheuniverse
  members:
    - "*"
...
```

### Read only / write
Here we want all users to have only the possibility to execute read only commands whereas the administrators will have access the the write commands.

`policies.yml`
```yml
---
readonly:
  all:
    ReadOnly:

readwrite:
  all:
    ReadWrite:
...
```

`groups.yml`
```yml
---
all:
  policies:
    - readonly
  members:
    - "*"

administrators:
  policies:
    - readwrite
  members:
    - rda
    - mal
...
```

### Restrict by container name
Here we want all users to have a limitation by the container name. All administrators are allowed to manage all containers.

`policies.yml`
```yml
---
containers_name_must_match_username:
  containers:
    containerNameCheck:
      startwith:
        - "$USER-"

readwrite:
  all:
    ReadWrite:
...
```

`groups.yml`
```yml
---
all:
  policies:
    - containers_name_must_match_username
  members:
    - "*"

administrators:
  policies:
    - readwrite
  members:
    - rda
    - mal
...
```

# Contribute

We will be pleased to receive your contribution as [Pull Request](https://github.com/docker-leash/leash-server/pulls) or as [Reported Issues](https://github.com/docker-leash/leash-server/issues).

You may want contribute to add new checks, see page [CONTRIBUTE](./CONTRIBUTE)
