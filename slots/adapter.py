# coding: utf-8

from assistant.adapters.logic.logic_adapter import LogicAdapter
from assistant.adapters.storage.storage_adapter import StorageAdapter

from trainer import SlotFillingTrainer


class SlotFillingAdapter(LogicAdapter):

    def __init__(self, intent, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)

        self.intent = intent
        self.storage = kwargs.get('storage', StorageAdapter())
        self.trainer = SlotFillingTrainer(self.storage)

    def can_process(self, statement):
        """
        main point is to check possibility of intent identification
        - check IntentData
        - check input statement

        :param statement: input statement
        :return: round possibility of intent detection
        """
        return True

    def process(self, statement):
        """
        main goal of this method is to detect parameters intent
        according to intent
        :param statement:
        :return:
        """
        raise self.AdapterMethodNotImplemented()
