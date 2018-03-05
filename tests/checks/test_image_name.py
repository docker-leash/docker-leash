# vim:set ts=4 sw=4 et:
'''
ImageNameTests
--------------
'''

import unittest

from docker_leash.checks.image_name import ImageName
from docker_leash.exceptions import (InvalidRequestException,
                                     UnauthorizedException,
                                     ConfigurationException)
from docker_leash.payload import Payload


PAYLOAD_BUILD_COMPLETE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/build?buildargs=%7B%7D&cachefrom=%5B%5D&cgroupparent=&cpuperiod=0&cpuquota=0&cpusetcpus=&cpusetmems=&cpushares=0&dockerfile=Dockerfile&labels=%7B%7D&memory=0&memswap=0&networkmode=default&rm=1&shmsize=0&t=test&target=&ulimits=null",
}

PAYLOAD_BUILD_UNDEFINED = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/build",
}

PAYLOAD_BUILD_FOOBAR = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/build?t=foobar",
}

PAYLOAD_BUILD_FOOBAR_TAG = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/build?t=foobar:something",
}

PAYLOAD_CREATE_PULL = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/create?fromImage=traefik&tag=alpine",
}

PAYLOAD_CREATE_IMPORT = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/create?fromSrc=-&message=&repo=traefik%3Aalpine&tag=",
}

PAYLOAD_INSPECT = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/traefik:alpine/json",
}

PAYLOAD_HISTORY = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/traefik:alpine/history",
}

PAYLOAD_PUSH = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/traefik/push?tag=alpine",
}


PAYLOAD_BUILD_PRIVATE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/build?t=registry.example.net/traefik:alpine",
}

PAYLOAD_HISTORY_PRIVATE = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/registry.example.net/traefik:alpine/history",
}

PAYLOAD_PUSH_PRIVATE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/registry.example.net/traefik/push?tag=alpine",
}

PAYLOAD_TAG = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/traefik:alpine/tag?repo=traefik2&tag=alpine2",
}

PAYLOAD_REMOVE = {
    "User": "someone",
    "RequestMethod": "DELETE",
    "RequestUri": "/v1.35/images/alpine:latest",
}

PAYLOAD_COMMIT = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/commit?author=&comment=&container=memcached&repo=alpine&tag=latest",
}

PAYLOAD_EXPORT = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/get?names=registry.example.net%2Ftraefik%3Aalpine",
}

PAYLOAD_EXPORT_SINGLE = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/registry.example.net/traefik:alpine/get",
}

PAYLOAD_EXPORT_MULTIPLE = {
    "User": "someone",
    "RequestMethod": "GET",
    "RequestUri": "/v1.35/images/get?names=registry.example.net%2Ftraefik%3Aalpine&names=mariadb",
}

PAYLOAD_CONTAINER_CREATE = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/containers/create?name=hard-biture",
    "RequestBody": {
        "Image": "registry.example.net:traefik:alpine",
    },
}

PAYLOAD_DUAL_NAME_1 = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/foo-foo:something/tag?repo=foo-bar&tag=something",
}

PAYLOAD_DUAL_NAME_2 = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/foo-bar:something/tag?repo=bar-baz&tag=something",
}

PAYLOAD_DUAL_SOMEONE_1 = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/someone-bar:something/tag?repo=someone-baz&tag=something",
}

PAYLOAD_DUAL_SOMEONE_2 = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/someone-bar:something/tag?repo=bar-baz&tag=something",
}

PAYLOAD_DUAL_SOMEONE_3 = {
    "User": "someone",
    "RequestMethod": "POST",
    "RequestUri": "/v1.35/images/foo-bar:something/tag?repo=someone-baz&tag=something",
}


class ImageNameTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.checks.ImageName`
    """

    def test_unconfigured_module(self):
        """Unconfigured module should return :exc:`ConfigurationException`
        """
        with self.assertRaises(ConfigurationException):
            ImageName().run(None, Payload(PAYLOAD_BUILD_UNDEFINED))

    def test_empty_payload(self):
        """Empty payload should return :exc:`InvalidRequestException`
        """
        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload({}))

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".+", Payload({}))

    def test_name_not_defined(self):
        """Without name return :exc:`InvalidRequestException`
        """
        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload(PAYLOAD_BUILD_UNDEFINED))

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".+", Payload(PAYLOAD_BUILD_UNDEFINED))

    def test_get_name_images_build(self):
        """Get name from image build
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_BUILD_COMPLETE))
        self.assertEqual(name, "test")
        self.assertEqual(tag, "latest")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_BUILD_FOOBAR))
        self.assertEqual(name, "foobar")
        self.assertEqual(tag, "latest")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_BUILD_FOOBAR_TAG))
        self.assertEqual(name, "foobar")
        self.assertEqual(tag, "something")

        with self.assertRaises(InvalidRequestException):
            ImageName()._get_name(Payload(PAYLOAD_BUILD_UNDEFINED))

    def test_get_name_images_create(self):
        """Get name from image create
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_CREATE_PULL))
        self.assertEqual(name, "traefik")
        self.assertEqual(tag, "alpine")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_CREATE_IMPORT))
        self.assertEqual(name, "traefik")
        self.assertEqual(tag, "alpine")

    def test_get_name_images_inspect(self):
        """Get name from image inspect
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_INSPECT))
        self.assertEqual(name, "traefik")
        self.assertEqual(tag, "alpine")

    def test_get_name_images_history(self):
        """Get name from image history
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_HISTORY))
        self.assertEqual(name, "traefik")
        self.assertEqual(tag, "alpine")

    def test_get_name_images_push(self):
        """Get name from image push
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_PUSH))
        self.assertEqual(name, "traefik")
        self.assertEqual(tag, "alpine")

    def test_get_name_images_tag(self):
        """Get name from image tag
        """
        [first, second] = ImageName()._get_name(Payload(PAYLOAD_TAG))
        self.assertEqual(first, ("traefik","alpine"))
        self.assertEqual(second, ("traefik2","alpine2"))

    def test_get_name_images_remove(self):
        """Get name from image remove
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_REMOVE))
        self.assertEqual(name, "alpine")
        self.assertEqual(tag, "latest")

    def test_get_name_images_commit(self):
        """Get name from image commit
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_COMMIT))
        self.assertEqual(name, "alpine")
        self.assertEqual(tag, "latest")

    def test_get_name_images_export(self):
        """Get name from image export
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_EXPORT))
        self.assertEqual(name, "registry.example.net/traefik")
        self.assertEqual(tag, "alpine")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_EXPORT_SINGLE))
        self.assertEqual(name, "registry.example.net/traefik")
        self.assertEqual(tag, "alpine")

    def test_get_name_images_export_multiple(self):
        """Get name from image export
        """
        [first, second] = ImageName()._get_name(Payload(PAYLOAD_EXPORT_MULTIPLE))
        self.assertEqual(first, ("registry.example.net/traefik","alpine"))
        self.assertEqual(second, ("mariadb","latest"))

    def test_get_name_images_for_private_registry(self):
        """Get name from image for private registry
        """
        name, tag = ImageName()._get_name(Payload(PAYLOAD_BUILD_PRIVATE))
        self.assertEqual(name, "registry.example.net/traefik")
        self.assertEqual(tag, "alpine")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_HISTORY_PRIVATE))
        self.assertEqual(name, "registry.example.net/traefik")
        self.assertEqual(tag, "alpine")

        name, tag = ImageName()._get_name(Payload(PAYLOAD_PUSH_PRIVATE))
        self.assertEqual(name, "registry.example.net/traefik")
        self.assertEqual(tag, "alpine")

    def test_tag_has_two_name(self):
        """The "tag" flag has two names
        """
        ImageName().run("^foo-.+", Payload(PAYLOAD_DUAL_NAME_1))
        ImageName().run(["^foo-.+"], Payload(PAYLOAD_DUAL_NAME_1))

        with self.assertRaises(UnauthorizedException):
            ImageName().run("^foo-.+", Payload(PAYLOAD_DUAL_NAME_2))

        with self.assertRaises(UnauthorizedException):
            ImageName().run(["^foo-.+"], Payload(PAYLOAD_DUAL_NAME_2))

    def test_tag_has_two_name_user(self):
        """Username replacement
        """
        ImageName().run("^$USER-.+", Payload(PAYLOAD_DUAL_SOMEONE_1))

        with self.assertRaises(UnauthorizedException):
            ImageName().run("^$USER-.+", Payload(PAYLOAD_DUAL_SOMEONE_2))

        with self.assertRaises(UnauthorizedException):
            ImageName().run("^$USER-.+", Payload(PAYLOAD_DUAL_SOMEONE_3))

        with self.assertRaises(UnauthorizedException):
            ImageName().run("^$USER-.+", Payload(PAYLOAD_DUAL_NAME_1))

    def test_invalid_query_parameter_compound_repo_name(self):
        """Missing repo name
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "POST",
            "RequestUri": "/v1.35/commit?tag=latest",
        }

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload(payload_invalid))

    def test_invalid_query_parameter_compound_tag(self):
        """Missing tag defaults to latest
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "POST",
            "RequestUri": "/v1.35/commit?repo=alpine",
        }

        ImageName().run(".*", Payload(payload_invalid))

    def test_path_and_query_parameter_missing_image_name(self):
        """Missing image name
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "POST",
            "RequestUri": "/v1.35/images//push?tag=alpine",
        }

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload(payload_invalid))

    def test_path_and_query_parameter_missing_tag_name(self):
        """Missing tag name
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "POST",
            "RequestUri": "/v1.35/images/traefik/push",
        }

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload(payload_invalid))

    def test_path_parameter_invalid_uri(self):
        """Invalid Uri
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "GET",
            "RequestUri": "/v1.35/images//history",
        }

        with self.assertRaises(InvalidRequestException):
            ImageName().run(".*", Payload(payload_invalid))

    def test_path_parameter_tag_default_to_latest(self):
        """Default tag is latest
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "GET",
            "RequestUri": "/v1.35/images/traefik/history",
        }

        ImageName().run(".*", Payload(payload_invalid))

    def test_ignore_action(self):
        """Ignore action
        """
        payload_invalid = {
            "User": "someone",
            "RequestMethod": "GET",
            "RequestUri": "/v1.35/containers/json",
        }

        self.assertIsNone(ImageName().run(".*", Payload(payload_invalid)))
