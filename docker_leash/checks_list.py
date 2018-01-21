# vim:set ts=4 sw=4 et:
'''
Checks
======
'''


class Checks(object):
    """The :class:`Checks` class is responsible for storing
    and deduplicating the checks to be launched.

    :var `docker_leash.checks_list.Checks.checks`: The check list.
    :vartype `docker_leash.checks_list.Checks.checks`: list
    """

    #:list: Internal storage of the checks to be applied.
    checks = None

    def __init__(self):
        self.checks = []

    def add(self, data):
        """Add a check to the list.

        If the same check is already in the list,
        it will silently be discarded.

        :param dict data: The check to append.
        """
        if data not in self:
            self.checks.append(self._structure_convert(data))

    @staticmethod
    def _structure_convert(data):
        """An internal helper that will convert structure
        from the configuration to a better internal format.

        :param dict data: The check to append.
                          It is a dictionary with a single key / value.
        :return: The reformatted test and arguments.
        :rtype: dict
        """
        if isinstance(data, str):
            return {'name': data, 'args': None}

        for key, val in data.iteritems():
            return {'name': key, 'args': val}

    def __contains__(self, data):
        """Validate presence of `data` in `self.checks`

        If data is `str` then check only the key.
        If data is `dict` then check the whole dict.
        """
        if isinstance(data, str):
            for item in self.checks:
                if data == item['name']:
                    return True
            return False

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
