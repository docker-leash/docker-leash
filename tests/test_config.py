# vim:set ts=4 sw=4 et:

import unittest

from app.config import Config

MOCKED_GROUPS = {
    "admins": {
        "policies": ["openbar"],
        "members": ["rda", "mal"]
    },
    "developpers": {
        "policies": ["restricted", "personnal"],
        "members": ["jre"]
    },
    "all": {
        "policies": ["readonly"],
        "members": ["*"]
    },
}

MOCKED_POLICIES = {
    "openbar": {
        "containersCreate": {
            "Allow": None
        }
    },
    "personnal": {
        "containersCreate": {
            "containerNameCheck": {
                "startwith": [
                    'foo',
                    'bar'
                ]
            },
            "pathCheck": [
                "+/mnt/usbkey"
            ],
            "Allow": None
        }
    },
    "restricted": {
        "containersCreate": {
            "pathCheck": [
                "-/",
                "+/home/$USER",
                "+/0"
            ],
            "Allow": None
        },
        "containersDelete": {
            "Deny": None
        },
    },
    "readonly": {
        "ping": {
            "Allow": None
        },
        "containersList": {
            "Allow": None
        }
    },
}


class ConfigTests(unittest.TestCase):

    def test_init(self):
        config = Config()
        self.assertEqual(config.policies, None)
        self.assertEqual(config.groups, None)

    def test_init_with_values(self):
        policies = {"foo": "foo"}
        groups = {"bar": "bar"}

        config = Config(policies=policies, groups=groups)
        self.assertEqual(config.policies, policies)
        self.assertEqual(config.groups, groups)

    def test_config_is_not_shared(self):
        policies1 = {"foo": "foo"}
        policies2 = {"bar": "bar"}

        groups1 = {"foo": "foo"}
        groups2 = {"bar": "bar"}

        config1 = Config(policies=policies1, groups=groups1)
        self.assertEqual(policies1, config1.policies)
        self.assertEqual(groups1, config1.groups)

        config2 = Config(policies=policies2, groups=groups2)
        self.assertEqual(policies2, config2.policies)
        self.assertEqual(groups2, config2.groups)

        self.assertNotEqual(policies1, config2.policies)
        self.assertNotEqual(groups1, config2.groups)

    def test_init_with_initial_values(self):
        policies1 = {"foo": "foo"}
        policies2 = {"bar": "bar"}
        groups1 = {"bar": "bar"}
        groups2 = {"bar": "bar"}

        z_policies = policies1.copy()
        z_policies.update(policies2)

        z_groups = groups1.copy()
        z_groups.update(groups2)

        config = Config(policies=policies1, groups=groups1)
        config.update(policies=policies2, groups=groups2)

        self.assertEqual(config.policies, z_policies)
        self.assertEqual(config.groups, z_groups)

    def test_get_groups_for_user_none(self):
        config = Config(groups=MOCKED_GROUPS)

        groups = config._get_groups_for_user(None)
        self.assertEqual(len(groups), 1)
        self.assertTrue('all' in groups)

    def test_get_groups_for_user_no_groups_defined(self):
        config = Config(groups=MOCKED_GROUPS)
        config.groups = None

        groups = config._get_groups_for_user(None)
        self.assertEqual(len(groups), 0)

    def test_get_groups_for_user(self):
        config = Config(groups=MOCKED_GROUPS)

        groups = config._get_groups_for_user('rda')
        self.assertEqual(len(groups), 2)
        self.assertTrue('all' in groups)
        self.assertTrue('admins' in groups)

        groups = config._get_groups_for_user('mal')
        self.assertEqual(len(groups), 2)
        self.assertTrue('all' in groups)
        self.assertTrue('admins' in groups)

        groups = config._get_groups_for_user('jre')
        self.assertEqual(len(groups), 2)
        self.assertTrue('all' in groups)
        self.assertTrue('developpers' in groups)

    def test_get_policies_for_user_none(self):
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        policies = config._get_policies_for_user(None)
        self.assertEqual(len(policies), 1)
        self.assertTrue('readonly' in policies)

    def test_get_policies_for_user(self):
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        policies = config._get_policies_for_user('rda')
        self.assertEqual(len(policies), 2)
        self.assertTrue('readonly' in policies)
        self.assertTrue('openbar' in policies)

        policies = config._get_policies_for_user('mal')
        self.assertEqual(len(policies), 2)
        self.assertTrue('readonly' in policies)
        self.assertTrue('openbar' in policies)

        policies = config._get_policies_for_user('jre')
        self.assertEqual(len(policies), 3)
        self.assertTrue('readonly' in policies)
        self.assertTrue('restricted' in policies)

    def test_get_checks_for_user(self):
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)
        checks = config.get_checks_for_user('jre', 'containersCreate')

        attended_result = [
            {
                "name": "containerNameCheck",
                "args": {'startwith': ['foo', 'bar']}
            },
            {
                "name": "pathCheck",
                "args": ["-/", "+/home/$USER", "+/0"]
            },
            {
                "name": "pathCheck",
                "args": ["+/mnt/usbkey"]
            },
            {
                "name": "Allow",
                "args": None
            },
        ]

        self.assertEqual(len(checks), 4)
        self.assertEqual(checks, attended_result)

    def test_get_policies_for_user_manual_config(self):
        groups = {
            'all': {
                'policies': ['allow_all'],
                'members': ['*']
            }
        }

        policies = {
            'allow_all': {
                'containersCreate': {
                    'allow': None
                }
            }
        }

        config = Config(groups, policies)

        policies = config._get_policies_for_user('rda')
        self.assertEqual(len(policies), 1)
        self.assertTrue('allow_all' in policies)

    def test_validate_action_name_exists(self):
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        self.assertEqual(len(config.get_checks_for_user('mal', 'someUnexistentAction')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersCreate')), 1)

    def test_validate_action_name_exists_with_the_any_action(self):

        groups = {
            "everyone": {
                "policies": ["openbar"],
                "members": ["*"]
            },
        }

        policies = {
            "openbar": {
                "any": {
                    "Allow": None
                }
            },
        }
        config = Config(groups, policies)
        self.assertEqual(len(config.get_checks_for_user('mal', 'any')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'someUnexistentAction')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersCreate')), 1)

    def test_validate_the_any_action(self):

        groups = {
            "everyone": {
                "policies": ["openbar"],
                "members": ["*"]
            },
        }

        policies = {
            "openbar": {
                "any": {
                    "Allow": None
                }
            },
        }
        config = Config(groups, policies)

        self.assertEqual(len(config.get_checks_for_user('mal', 'containersCreate')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersRemove')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'imagesList')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'networksPrune')), 1)

    def test_validate_the_readonly_action(self):

        groups = {
            "everyone": {
                "policies": ["readonly"],
                "members": ["*"]
            },
        }

        policies = {
            "readonly": {
                "readOnly": {
                    "Allow": None
                }
            },
        }
        config = Config(groups, policies)

        self.assertEqual(len(config.get_checks_for_user('mal', 'containersList')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'imagesList')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'systemPing')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'volumesList')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'secretsList')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersCreate')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersRemove')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'networksPrune')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'pluginsInstall')), 0)

    def test_validate_the_readwrite_action(self):

        groups = {
            "everyone": {
                "policies": ["readonly"],
                "members": ["*"]
            },
        }

        policies = {
            "readonly": {
                "readWrite": {
                    "Allow": None
                }
            },
        }
        config = Config(groups, policies)

        self.assertEqual(len(config.get_checks_for_user('mal', 'containersList')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'imagesList')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'systemPing')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'volumesList')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'secretsList')), 0)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersCreate')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'containersRemove')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'networksPrune')), 1)
        self.assertEqual(len(config.get_checks_for_user('mal', 'pluginsInstall')), 1)
