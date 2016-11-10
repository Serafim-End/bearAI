# coding: utf-8

from assistant.adapters.adapter import Adapter


class LogicAdapter(Adapter):

    def can_process(self, statement):
        """
        :param statement: process depends on Statement and of course checking
         of process depends on Statement too
        :return: is it possible to process
        """
        return True

    def process(self, statement):
        raise self.AdapterMethodNotImplemented()

    class EmptyDatasetException(Exception):

        def __init__(self, value='An empty data set.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
