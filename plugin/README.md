# Install the client

On `docker daemon` side (the client in our case), the plugin configuration
consist of a simple `.json` file. Copy `leash.json` to the `/etc/docker/plugins`
or `/usr/lib/docker/plugins` directory.

## Configure the plugin

The `/usr/lib/docker/plugins/leash.json` file need to be configured according to
your local environment.

```
$ cat /usr/lib/docker/plugins/leash.json
{
  "Name": "leash",
  "Addr": "https://leash-server.organization.yours",
  "TLSConfig": {
    "InsecureSkipVerify": false,
    "CAFile": "/usr/shared/docker/certs/example-ca.pem",
    "CertFile": "/usr/shared/docker/certs/example-cert.pem",
    "KeyFile": "/usr/shared/docker/certs/example-key.pem"
  }
}
```

Replace the `Addr` field with the full url of your leash `leash server`
instance. If you secured the server part with `TLS`, declare the `CA` in the
`CAFile` field.

Note: The fields `CertFile` and `KeyFile` are present in the
[docker documentation](https://docs.docker.com/engine/extend/plugin_api/#json-specification),
but unfortunately they are not documented...

Even if - on a security point of view - this is not recommended, you could also
choose to not verify the authenticity of the connection, by setting field
`InsecureSkipVerify` to the `true` value.

```
$ cat /usr/lib/docker/plugins/leash.json
{
  "Name": "leash",
  "Addr": "https://leash-server.organization.yours",
  "TLSConfig": {
    "InsecureSkipVerify": true
  }
}
```

## Start the plugin

The `docker daemon` need to start the plugin on boot. You have many
possibilities depending on how you launch the docker daemon (ex `systemd`), but
the simplest way seems to configure it directly in the `/etc/docker/daemon.json`.

Add the `authorization-plugins` entry as:

```
$ cat /etc/docker/daemon.json
{
	"authorization-plugins": ["leash"].
  [...]
}
```

A more complete example:
```
$ cat /etc/docker/daemon.json
{
	"authorization-plugins": ["leash"],
	"hosts": ["unix:///var/run/docker.sock", "0.0.0.0:2376"],
	"tls": true,
	"tlsverify": true,
	"tlscacert": "/etc/pki/CA/certs/company.crt",
	"tlscert": "/etc/pki/tls/certs/dockerhost.crt",
	"tlskey": "/etc/pki/tls/private/dockerhost.key"
}
```

Notes: `tlscacert` refer to the `Certificate Authority` you will generate later.
It will permit to validate and accept connections using `clients certificates`.
The `tlscert` and `tlskey` pair will allow to check the authenticity of the
connection from the `docker clients` to the `docker daemon`.

# Users authentication

In our case, for advanced features, users to the `docker daemon` need to
authenticate. You have to generate a `Certificate Authority` and `clients certificates`.

Your best bet is to follow instructions from the official docker documentation.
https://docs.docker.com/engine/security/https/#create-a-ca-server-and-client-keys-with-openssl

## Manage your CA using EasyRSA

TBD

## Configure user docker client

Once you have generated `clients certificates`, place in the user's (`$HOME/.docker/`)
directory the `ca.pem` (used to authenticate `dockerd`), and `cert.pem` + `key.pem`.

Note: use explicitly that names.
