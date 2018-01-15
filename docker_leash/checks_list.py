# vim:set ts=4 sw=4 et:


class Checks(object):
    """The :class:`docker_leash.checks_list.Checks` class is responsible for storing and deduplicating the checks to be launched.

    :var `docker_leash.checks_list.Checks.checks`: The check list.
    :vartype `docker_leash.checks_list.Checks.checks`: list
    """

    #:list: Internal storage of the checks to be applied.
    checks = None

    def __init__(self):
        self.checks = []

    def add(self, data):
        """Add a check to the list.

        If the same check is already in the list, it will silently be discarded.

        :param dict data: The check to append.
        """
        if data not in self:
            self.checks.append(self._structure_convert(data))

    @classmethod
    def _structure_convert(cls, data):
        """An internal helper that will convert structure from the configuration to a better internal format.

        :param dict data: The check to append.
        :return: The reformatted test and arguments.
        :rtype: dict
        """
        for k, v in data.iteritems():
            return {'name': k, 'args': v}

    def __contains__(self, data):
        _data = self._structure_convert(data)
        for item in self.checks:
            if _data == item:
                return True
        return False

    def __getitem__(self, key):
        return self.checks.__getitem__(key)

    def __len__(self):
        return len(self.checks)

    def __eq__(self, other):
        return self.checks.sort() == other.sort()

    def __repr__(self):
        return self.checks.__repr__()
