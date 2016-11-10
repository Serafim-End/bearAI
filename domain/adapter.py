# coding: utf-8

from assistant.adapters.logic.logic_adapter import LogicAdapter
from assistant.adapters.storage.storage_adapter import StorageAdapter
from assistant.trainer import Trainer

from trainer import DomainTrainer


class DomainAdapter(LogicAdapter):

    def __init__(self, agent, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)

        self.agent = agent
        self.storage = kwargs.get('storage', StorageAdapter())
        self.trainer = DomainTrainer(self.storage)

    def can_process(self, statement):
        """
        check what domain can be detected
        - check data
        - check statement

        :param statement:
        :return:
        """
        return True

    def process(self, statement):
        """
        detect domain according to agent - main goal of this adapter
        :param statement:
        :return:
        """
        raise self.AdapterMethodNotImplemented()

    def update_domain_data(self):
        raise NotImplementedError()

    def set_trainer(self, trainer):

        if isinstance(trainer, Trainer):
            self.trainer = trainer

        else:
            raise TypeError
