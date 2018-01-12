# vim:set ts=4 sw=4 et:


class Checks():

    checks = None

    def __init__(self):
        self.checks = []

    def add(self, data):
        if data not in self:
            self.checks.append(self._structure_convert(data))

    def _structure_convert(self, data):
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
