# coding: utf-8

from assistant.adapters.adapter import Adapter


class InputDevAdapter(Adapter):

    def process_input(self):
        raise self.AdapterMethodNotImplemented()


class InputAdapter(Adapter):

    def process_input(self, input_sequence):
        raise self.AdapterMethodNotImplemented()
