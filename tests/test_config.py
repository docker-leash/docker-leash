# vim:set ts=4 sw=4 et:
'''
ConfigTests
===========
'''

import unittest

from docker_leash.config import Config
from docker_leash.exceptions import ConfigurationException
from docker_leash.leash_server import app
from docker_leash.payload import Payload

MOCKED_GROUPS = {
    "admins": ["rda", "mal"],
    "users": ["jre", "lgh", "dga", "ore", "pyr"],
    "monitoring": ["xymon_1", "xymon_2"],
    "anonymous": ["Anonymous"],
    "all": ["*"],
}

MOCKED_POLICIES = [
    {
        "description": "Servers are fully accessible to Admins.",
        "hosts": [r"+^srv\d\d.*", r"-^srv3\d.*", r"+^srv38.*"],
        "default": "Deny",
        "policies": [
            {
                "members": ["admins"],
                "rules": {
                    "any": {
                        "Allow": None
                    }
                }
            },
            {
                "members": ["monitoring"],
                "rules": {
                    "containersList": {
                        "Allow": None
                    }
                }
            },
        ],
    },
    {
        "description": "Users have access to containers and images starting by their name.",
        "hosts": [r"+^wks\d\d.*"],
        "default": "ReadOnly",
        "policies": [
            {
                "members": ["admins"],
                "rules": {
                    "any": {
                        "Allow": None
                    }
                }
            },
            {
                "members": ["users"],
                "rules": {
                    "containersLogs": {
                        "ContainerName": [
                            "^bar-",
                            "^foo-",
                            "^$USER-"
                        ]
                    },
                    "containers": {
                        "ContainerName": [
                            "^foo-",
                            "^$USER-"
                        ],
                        "ImagesName": [
                            "^foo-",
                            "^$USER-"
                        ],
                        "BindVolumes": [
                            "-/",
                            "+/home/$USER",
                            "+/0"
                        ],
                    },
                    "imagesCreate": {
                        "ImagesName": [
                            "^foo-",
                            "^$USER-"
                        ],
                    },
                },
            },
        ],
    },
    {
        "description": "Deny access to Anonymous users.",
        "hosts": [r"+.*"],
        "default": "ReadOnly",
        "policies": [
            {
                "members": ["admins"],
                "rules": {
                    "any": {
                        "Allow": None
                    }
                }
            },
            {
                "members": ["anonymous"],
                "rules": {
                    "any": {
                        "Deny": None
                    }
                }
            },
        ],
    },
]


class ConfigTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.Config`
    """

    def setUp(self):
        app.config['DEBUG'] = False

    def test_init(self):
        """Empty config should not raise any error
        """
        config = Config()
        self.assertEqual(config.policies, None)
        self.assertEqual(config.groups, None)

    def test_init_with_values(self):
        """Store and read arbitrary config
        """
        policies = {"foo": "foo"}
        groups = {"bar": "bar"}

        config = Config(policies=policies, groups=groups)
        self.assertEqual(config.policies, policies)
        self.assertEqual(config.groups, groups)

    def test_config_is_not_shared(self):
        """Config objects must not share config
        """
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

    def test_default_rule(self):
        """Retrieve default rule
        """
        ruleset1 = Config._default_rule({"default": "Deny"})
        ruleset2 = Config._default_rule({"default": "Allow"})

        self.assertEqual(ruleset1[0]["name"], "Deny")
        self.assertEqual(ruleset2[0]["name"], "Allow")
        self.assertEqual(ruleset1[0]["name"], "Deny")
        self.assertEqual(ruleset2[0]["name"], "Allow")

    def test_get_policy_by_member(self):
        """Retrieve policy group by member
        """
        policies = [
            {
                "members": ["admins"],
                "rules": "_administrators"
            },
            {
                "members": ["anonymous"],
                "rules": "_anonymous"
            },
        ]
        groups = {
            "admins": ["rda", "mal"],
            "anonymous": ["Anonymous"],
        }
        config = Config(groups=groups)

        self.assertEqual(config._get_policy_by_member(None, policies), "_anonymous")
        self.assertEqual(config._get_policy_by_member("mal", policies), "_administrators")
        self.assertEqual(config._get_policy_by_member("jre", policies), None)

    def test_match_host(self):
        """Verify host matcher
        """
        with self.assertRaises(ConfigurationException):
            self.assertTrue(Config._match_host("srv01", [r".*"]))

    def test_get_rules_for_anonymous_1(self):
        """An anonymous user cannot create containers on server
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Deny', rules)

    def test_get_rules_for_anonymous_2(self):
        """An anonymous user cannot create containers on workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_anonymous_3(self):
        """An anonymous user cannot create containers on other hosts
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": None,
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "other01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Deny', rules)

    def test_get_rules_for_admin_1(self):
        """An admin can create containers on servers
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Allow', rules)

    def test_get_rules_for_admin_2(self):
        """An admin can create containers on workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Allow', rules)

    def test_get_rules_for_admin_3(self):
        """An admin can create containers on other hosts
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "other01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Allow', rules)

    def test_get_rules_for_admin_4(self):
        """Host srv33 is considered as other
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "mal",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv33",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Allow', rules)

    def test_get_rules_for_user_1(self):
        """A normal user cannot create containers on servers
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Deny', rules)

    def test_get_rules_for_user_2(self):
        """A normal user can create containers on workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 3)
        self.assertIn('ContainerName', rules)
        self.assertIn('ImagesName', rules)
        self.assertIn('BindVolumes', rules)

    def test_get_rules_for_user_3(self):
        """A normal user can only get logs for certain containers
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/containers/123/logs",
            "Host": "wks01",
        })
        expected = {
            "ContainerName": [
                "^bar-",
                "^foo-",
                "^$USER-"
            ]
        }

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn(expected, rules)

    def test_get_rules_for_user_4(self):
        """A normal user can create images on workstation only with specific names
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/images/create",
            "Host": "wks01",
        })
        expected = {
            "ImagesName": [
                "^foo-",
                "^$USER-"
            ]
        }

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn(expected, rules)

    def test_get_rules_for_user_5(self):
        """A normal user can list images on workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/images/json",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_user_6(self):
        """A normal user cannot delete images on a workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/images/abc123",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_user_7(self):
        """A normal user cannot delete images on a workstation
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/images/abc123",
            "Host": "wks01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_user_8(self):
        """A normal user cannot list images on other hosts
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "GET",
            "RequestUri": "/v1.32/images/json",
            "Host": "other01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_user_9(self):
        """A normal user cannot list images on other hosts
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "DELETE",
            "RequestUri": "/v1.32/images/abc123",
            "Host": "other01",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_get_rules_for_user_10(self):
        """A normal user can list images on srv33
        """
        config = Config(policies=MOCKED_POLICIES, groups=MOCKED_GROUPS)

        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv33",
        })

        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('ReadOnly', rules)

    def test_policyless_allow(self):
        """The most simple policy
        """
        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv33",
        })

        policy_allow = [
            {
                "description": "Allow everything.",
                "hosts": [r"+.*"],
                "default": "Allow",
            }
        ]

        config = Config(policies=policy_allow)
        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Allow', rules)

    def test_policyless_deny(self):
        """The most simple policy
        """
        payload = Payload({
            "User": "jre",
            "RequestMethod": "POST",
            "RequestUri": "/v1.32/containers/create",
            "Host": "srv33",
        })

        policy_deny = [
            {
                "description": "Deny everything.",
                "hosts": [r"+.*"],
                "default": "Deny",
            }
        ]

        config = Config(policies=policy_deny)
        rules = config.get_rules(payload)
        self.assertEqual(len(rules), 1)
        self.assertIn('Deny', rules)


#####


data_match_rules = (
    (
        {
            "containersLogs": {"ContainerName": "Allow"},
            "containers": {"ContainerName": "Allow", "ImagesName": "Allow"},
        },
        (
            ("GET", "/containers/test-data/logs", 1),
            ("POST", "/images/create", 0),
            ("POST", "/containers/create", 2),
            ("GET", "/images/json", 0),
        ),
    ),
    (
        {
            "containersLogs": {"ContainerName": "Allow"},
            "containers": {"ContainerName": "Allow", "ImagesName": "Allow"},
            "any": {"imagesCreate": "Allow"},
        },
        (
            ("GET", "/containers/test-data/logs", 1),
            ("POST", "/containers/create", 2),
            ("POST", "/images/create", 1),
            ("GET", "/images/json", 1),
        ),
    ),
)


def create_match_rules(actions, method, query, expect):
    def do_test(self):
        """Verify rules matcher
        """
        result = len(Config._match_rules(action_name, actions))
        self.assertEqual(
            result,
            expected,
            'expected: {!r}, got: {!r}'.format(expect, result)
        )
    return do_test


i = 0
for actions, checks in data_match_rules:
    for check in checks:
        func = create_match_rules(actions, *check)
        func.__name__ = 'create_match_rules_{:02d}'.format(i)
        setattr(ConfigTests, func.__name__, func)
        i += 1
del func

data_match_host = (
    (
        [r"+^srv\d\d.*", r"-^srv3\d.*", r"+^srv38.*"],
        (
            ("srv01", True),
            ("srv02", True),
            ("srv36", False),
            ("srv38", True),
            ("wks01", False),
            ("wks02", False),
            ("other01", False),
        ),
    ),
    (
        [r"+^wks\d\d.*"],
        (
            ("srv01", False),
            ("srv02", False),
            ("srv36", False),
            ("wks01", True),
            ("wks02", True),
            ("other01", False),
        ),
    ),
    (
        [r"+.*"],
        (
            ("srv01", True),
            ("srv02", True),
            ("srv36", True),
            ("wks01", True),
            ("wks02", True),
            ("other01", True),
        ),
    ),
)


def create_match_host(hosts, host, expect):
    def do_test(self):
        """Verify host matcher
        """
        getattr(self, 'assert{}'.format(expect))(
            Config._match_host(host, hosts)
        )
    return do_test


i = 0
for hosts, checks in data_match_host:
    for check in checks:
        func = create_match_host(hosts, *check)
        func.__name__ = 'create_match_host_{:02d}'.format(i)
        setattr(ConfigTests, func.__name__, func)
        i += 1

# nosetests compatibility workaround
del func
