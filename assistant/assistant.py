# coding: utf-8

import logging

from adapters.storage.storage_adapter import StorageAdapter
from adapters.input.crm_adapter import InputAdapter
from adapters.output.output_format_adapter import OutputFormatAdapter
from adapters.logic.multi_adapter import MultiLogicAdapter


class Assistant(object):

    """
    may be preprocess function should be added in separated adapter
    """

    def __init__(self, **kwargs):

        # input_adapter = some input adapter based on Inputadapter
        # (may be CRMAdapter, but not necessary )

        # storage_adapter = some storage adapter based on BaseStorageAdapter

        # output_adapter = some output adapter based on OutputFormatAdapter

        # logic adapters = stack of adapters in organized queue

        self.input = InputAdapter(**kwargs)
        self.storage = StorageAdapter(**kwargs)
        self.output = OutputFormatAdapter(**kwargs)
        self.logic = MultiLogicAdapter(**kwargs)

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

        # self.trainer = train dialog - response of bot,
        # but only collecting data only

    def add_adapter(self, adapter):
        raise NotImplementedError()

    def remove_adapter(self, adapter):
        raise NotImplementedError()

    def validate_adapter(self, adapter_class):
        raise NotImplementedError()

    def response(self):
        raise NotImplementedError()

    # def train(self):
    #     pass

    class InvalidAdapterException(Exception):

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)