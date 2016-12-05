# coding: utf-8

from assistant.context_manager import ContextManager
from assistant.adapters.storage.storage_adapter import StorageAdapter
from assistant.task import Task

from assistant_custom.adapters.domain_adapter import CustomDomainAdapter


class CustomContextManager(ContextManager):

    def __init__(self, statement, task, **kwargs):
        super(CustomContextManager, self).__init__(statement, task)

        self.status = kwargs.get('status')
        # about db
        self.storage = StorageAdapter(**kwargs)

    def detect_task_status(self,):
        if not self.task:
            self.create_new_task()

    def create_new_task(self, **kwargs):

        domain_adapter = CustomDomainAdapter(**kwargs)

        if domain_adapter.can_process(self.statement):
            self.task.domain = domain_adapter.process(self.statement)

        if self.task.domain:
            pass
