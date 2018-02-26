# vim:set ts=4 sw=4 et:
'''
ValidateExample5Functionnal
---------------------------
'''

import base64
import json

from . import is_success, post
from .test_base import LeashServerFunctionnalBaseTests


class ValidateExample5Functionnal(LeashServerFunctionnalBaseTests):
    """Functionnal validation of the documented example 5
    """

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        :param `Flask` application: The current flask application
        """
        example_dir = "./docs/examples/configs/example_5"
        application.config['GROUPS_FILE'] = example_dir + "/groups.yml"
        application.config['POLICIES_FILE'] = example_dir + "/policies.yml"

    def test_servers_1(self):
        """Servers are restricted to admin only: admin
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_servers_2(self):
        """Servers are restricted to admin only: user
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "jre",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_servers_3(self):
        """Servers are restricted to admin only: user not from any group
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "vol",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_servers_4(self):
        """Servers are restricted to admin only: anonymous
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "Host": "srv01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_1(self):
        """Workstations are restricted to connected users or admins: admin
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_wks_2(self):
        """Workstations are restricted to connected users or admins: user
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_wks_3(self):
        """Workstations are restricted to connected users or admins: someone
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "vol",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_4(self):
        """Users from `users` group can only manage containers: user
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/abc123",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_wks_5(self):
        """Users from `users` group can only manage containers: someone
        """
        payload = {
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/containers/abc123",
            "User": "vol",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_6(self):
        """Users from `users` group can only manage images: user
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/images/json",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_wks_7(self):
        """Users from `users` group can only manage images: someone
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/images/json",
            "User": "vol",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_8(self):
        """Bind mounts are restricted to `/home/$USER/`: /
        """
        request = {
            "HostConfig": {
                "Binds": [
                    "/:/mnt/foo:rw"
                ]
            }
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_9(self):
        """Bind mounts are restricted to `/home/$USER/`: /home
        """
        request = {
            "HostConfig": {
                "Binds": [
                    "/home:/mnt/foo:rw"
                ]
            }
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_10(self):
        """Bind mounts are restricted to `/home/$USER/`: /home/$USER
        """
        request = {
            "HostConfig": {
                "Binds": [
                    "/home/jre:/mnt/foo:rw"
                ]
            }
        }
        payload = {
            "RequestBody": base64.b64encode(json.dumps(request)),
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_wks_11(self):
        """All other actions are read-only: list volumes
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/volumes",
            "User": "jre",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_12(self):
        """Unauthenticated users cannot do anything: list volumes
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/volumes",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_wks_13(self):
        """Unauthenticated users cannot do anything: list containers
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "Host": "wks01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_1(self):
        """All other hosts are read-only even for admins: readonly as admin
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "mal",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_other_2(self):
        """All other hosts are read-only even for admins: readonly as user
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "jre",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_other_3(self):
        """All other hosts are read-only even for admins: readonly as someone
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "User": "vol",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_other_4(self):
        """All other hosts are read-only even for admins: readonly as anonymous
        """
        payload = {
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/json",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_success(response))

    def test_other_write_1(self):
        """All other hosts are read-only even for admins: write as admin
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/images/create",
            "User": "mal",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_write_2(self):
        """All other hosts are read-only even for admins: write as user
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/images/create",
            "User": "jre",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_write_3(self):
        """All other hosts are read-only even for admins: write as someone
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/images/create",
            "User": "vol",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))

    def test_other_write_4(self):
        """All other hosts are read-only even for admins: write as anonymous
        """
        payload = {
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/images/create",
            "Host": "other01",
        }

        response = post(self.app, payload)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(is_success(response))
