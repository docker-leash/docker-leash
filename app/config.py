# vim:set ts=4 sw=4 et:

from app.checks_list import Checks


class Config(object):
    policies = None
    groups = None

    def __init__(self, groups=None, policies=None):
        self.update(groups, policies)

    def update(self, groups=None, policies=None):
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
        groups = []

        if not self.groups:
            return groups

        for group_name, group in self.groups.iteritems():
            if '*' in group['members'] or user in group['members']:
                groups.append(group_name)
        return groups

    def _get_policies_for_user(self, user):
        groups = self._get_groups_for_user(user)
        policies = []
        for group in groups:
            policies.extend(self.groups[group]['policies'])
        return policies

    def get_checks_for_user(self, user, action):
        policies = self._get_policies_for_user(user)
        checks = Checks()

        for policy in policies:
            if action in self.policies[policy]:
                for k, v in self.policies[policy][action].iteritems():
                    checks.add({k: v})
        return checks
