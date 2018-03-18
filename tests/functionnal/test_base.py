# vim:set ts=4 sw=4 et:
'''
LeashServerFunctionnalBaseTests
-------------------------------
'''

import os
import unittest

from docker_leash.leash_server import application


class LeashServerFunctionnalBaseTests(unittest.TestCase):
    """Base class for functionnal tests
    """

    @classmethod
    def setUpClass(cls):
        """Define action to be launched once per class
        """
        cls.set_conf_files(application)
        application.config["processor"].load_config()

    def setUp(self):
        """Define action to be launched once per test
        """
        self.app = application.test_client()

    def tearDown(self):
        """Define action to be launched once after each test
        """
        pass

    @staticmethod
    def set_conf_files(application):
        """Define config file to read

        Override it in other tests to load different configurations

        :param `Flask` application: The current flask application
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        application.config['GROUPS_FILE'] = dir_path + "/mocked_configs/groups.yml"
        application.config['POLICIES_FILE'] = dir_path + "/mocked_configs/policies.yml"
