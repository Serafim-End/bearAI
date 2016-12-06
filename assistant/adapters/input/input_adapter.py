# coding: utf-8

from assistant.adapters.adapter import Adapter


class InputDevAdapter(Adapter):

    def process_input(self):
        raise self.AdapterMethodNotImplemented()


class InputAdapter(Adapter):

    def process_input(self, input_sequence, **kwargs):
        """
        it is an instance of Statement model that have put already in db
        :param input_sequence: message and customer (id) in kwargs
        :return:
        """
        raise self.AdapterMethodNotImplemented()
