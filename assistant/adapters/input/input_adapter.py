# coding: utf-8

from assistant.adapters.adapter import Adapter


class InputAdapter(Adapter):

    def process_input(self):
        raise self.AdapterMethodNotImplemented()
