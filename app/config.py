# vim:set ts=4 sw=4 et:

from app.action_mapper import ActionMapper
from app.checks_list import Checks


class Config(object):
    """The :class:`Config` class is responsible for storing application groups and polcies read from the datastore.

    It has some handy functions to extract values from the configuration. It can respond to questions such as:
    "Which are the groups for a user?", "Which policies user belong to?", "Which tests are enabled for a user?".

    :var groups: The groups.
    :vartype groups: dict or None
    :var policies: The policies.
    :vartype policies: dict or None

    :param groups: The groups.
    :type groups: dict or None
    :param policies: The policies.
    :type policies: dict or None
    """

    #: The loaded policies
    policies = None

    #: The loaded groups
    groups = None

    def __init__(self, groups=None, policies=None):
        self.update(groups, policies)

    def update(self, groups=None, policies=None):
        """Update the stored configuration with the provided values.

        :param groups: The groups.
        :type groups: dict or None
        :param policies: The policies.
        :type policies: dict or None
        """
        if groups:
            if self.groups:
                self.groups.update(groups)
            else:
                self.groups = groups

        if policies:
            if self.policies:
                self.policies.update(policies)
            else:
                self.policies = policies

    def _get_groups_for_user(self, user):
        """Return the groups a user belongs to.

        :param string user: The username to get groups.
        :return: The groups list the user belongs to.
        :rtype: list
        """
        groups = []

        if not self.groups:
            return groups

        for group_name, group in self.groups.iteritems():
            if '*' in group['members'] or user in group['members']:
                groups.append(group_name)
        return groups

    def _get_policies_for_user(self, user):
        """Return the policies to be applied for a user.

        :param string user: The username to get policies.
        :return: The policies list to be applied.
        :rtype: list
        """
        groups = self._get_groups_for_user(user)
        policies = []
        for group in groups:
            policies.extend(self.groups[group]['policies'])
        return policies

    def get_checks_for_user(self, user, action):
        """Return the :mod:`app.checks` to be applied for an user and an action.

        :param string user: The username.
        :param string action: The action to compare.
        :return: The :mod:`app.checks` list to be verified against a payload.
        :rtype: list
        """
        policies = self._get_policies_for_user(user)
        checks = Checks()
        mapper = ActionMapper()

        if mapper.is_action(action):
            for policy in policies:

                # Look for "normal" Actions
                if action in self.policies[policy]:
                    for k, v in self.policies[policy][action].iteritems():
                        checks.add({k: v})

                # Look for "any" Actions
                elif 'any' in self.policies[policy].keys():
                    for k, v in self.policies[policy]['any'].iteritems():
                        checks.add({k: v})

                # Look for "readonly" Actions
                elif 'readOnly' in self.policies[policy].keys():
                    if mapper.is_readonly(action):
                        for k, v in self.policies[policy]['readOnly'].iteritems():
                            checks.add({k: v})

                # Look for "readwrite" Actions
                elif 'readWrite' in self.policies[policy].keys():
                        if not mapper.is_readonly(action):
                            for k, v in self.policies[policy]['readWrite'].iteritems():
                                checks.add({k: v})

        return checks
