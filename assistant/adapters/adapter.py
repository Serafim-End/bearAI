# coding: utf-8


class Adapter(object):
    def __init__(self, **kwargs):
        """
        :param kwargs: any parameters for every Adapter
        :return:
        """
        self.context = None

    def set_context(self, context):
        self.context = context

    class AdapterMethodNotImplemented(NotImplementedError):
        def __init__(self, message='must be overriden in a subclass method'):
            self.message = message

        def __str__(self):
            return self.message
