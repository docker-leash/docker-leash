# vim:set ts=4 sw=4 et:


class BaseCheck():

    def run(self, config, payload):
        raise NotImplementedError(
            "'run' mot implemented in module `%s`" % self.__class__.__name__
        )
