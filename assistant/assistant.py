# coding: utf-8

import logging

from adapters.storage.storage_adapter import StorageAdapter
from adapters.input.input_adapter import InputAdapter
from adapters.output.output_format_adapter import OutputFormatAdapter
from adapters.logic.multi_adapter import MultiLogicAdapter
from adapters.logic.logic_adapter import LogicAdapter
from context_manager import ContextManager
from task import Task

from utils.module_loading import import_loading


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

        input_class = kwargs.get('input_class')
        if input_class:
            self.input = import_loading(input_class)(**kwargs)
        else:
            self.input = InputAdapter(**kwargs)

        storage_class = kwargs.get('storage_class')
        if storage_class:
            self.storage = import_loading(storage_class)(**kwargs)
        else:
            self.storage = StorageAdapter(**kwargs)

        output_class = kwargs.get('output_class')
        if output_class:
            self.output = import_loading(output_class)(**kwargs)
        else:
            self.output = OutputFormatAdapter(**kwargs)

        context_manager_class = kwargs.get('context_manager')
        if context_manager_class:
            self.context_manager_class = import_loading(context_manager_class)
        else:
            self.context_manager_class = ContextManager

        self.logic = MultiLogicAdapter(**kwargs)
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        # initialize domain and intent trainers
        self.initialize_trainers()

        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

        # self.trainer = train dialog - response of bot,
        # but now we only can collect data

    def add_adapter(self, logic_adapter, order_index, **kwargs):
        self.validate_adapter(import_loading(logic_adapter), LogicAdapter)

        CustomAdapter = import_loading(logic_adapter)
        instance_adapter = CustomAdapter(**kwargs)

        self.logic.add_adapter(instance_adapter, order_index)

    def remove_adapter(self, adapter):
        for i, a in enumerate(self.logic.adapters):
            if adapter == type(a).__name__:
                del(self.logic.adapters[i])
                return True
        return False

    def validate_adapter(self, validate_class, adapter_class):
        from .adapters import Adapter

        if not issubclass(import_loading(validate_class), Adapter):
            raise self.InvalidAdapterException(
                'class {} is not adapter class'.format(
                    validate_class.__name__
                )
            )

        if not issubclass(import_loading(adapter_class), adapter_class):
            raise self.InvalidAdapterException(
                'class {} is not an {} class {}'.format(
                    validate_class.__name__,
                    adapter_class.__name__
                )
            )

    def response(self, input_seq):
        input_statement = self.input.process_input(input_seq)

        # get status of the task from db, session table
        # task = ??? data about the task (class Task)
        task = self.storage.get_task(input_statement.customer)
        context_manager = self.context_manager_class(
            statement=input_statement,
            task=task,
            domain_trainer=self.domain_trainer,
            intent_trainer=self.intent_trainer,
            word2vec_trainer=self.word2vec_trainer,
            storage=self.storage
        )

        context_manager.process_task()

        self.storage.set_task(task, input_statement.customer)
        return self.output.process_response()

    def initialize_trainers(self):
        import cPickle as pickle

        def load_model(filename, mode='r'):
            try:
                with open(filename, mode) as model_file:
                    return pickle.load(model_file)
            except Exception as e:
                raise Exception(
                    'error in model {} loading with message: {}'.format(
                        filename, e.message
                    )
                )

        self.domain_trainer = load_model('domain_trainer')
        self.word2vec_trainer = load_model('word2vec_trainer')
        self.intent_trainer = load_model('intent_trainer')

    class InvalidAdapterException(Exception):

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)