# coding: utf-8

from assistant.adapters.adapter import Adapter


class OutputAdapter(Adapter):

    def process_input(self, input, confidence):
        """
        :param input: input value
        :param confidence: confidence to check adequacy of output
        :return:
        """
        raise self.AdapterMethodNotImplemented()
