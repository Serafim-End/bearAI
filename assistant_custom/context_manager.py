# coding: utf-8

from assistant.context_manager import ContextManager
from assistant.adapters.storage.storage_adapter import StorageAdapter

from assistant_custom.adapters.domain_adapter import CustomDomainAdapter
from assistant_custom.adapters.intent_adapter import CustomIntentAdapter
from assistant_custom.adapters.slots_adapter import CustomSlotFillingAdapter


class CustomContextManager(ContextManager):

    def __init__(self, statement, task, **kwargs):
        super(CustomContextManager, self).__init__(statement, task)

        self.status = kwargs.get('status')

        # about db
        self.storage = kwargs.get('storage')
        if not self.storage:
            self.storage = StorageAdapter(**kwargs)

        self.domain_adapter = CustomDomainAdapter(
            trainer=kwargs.get('domain_trainer'),
            storage=self.storage,
            **kwargs
        )

        # do not think that it is normal
        self.kwargs = kwargs

    def process_task(self):
        """
        what kind of status exist ?
        status = True mean that status is active and false otherwise
        :return: precess the task
        """

        # if task is finished we should not process it
        if not self.status:
            return self.task

        # if status is active it is mean that
        #  task have already had filled fields
        # Order of filling: domain -> intent -> parameters
        # in this logic domain should not be empty

        if not self.task.domain:
            if self.domain_adapter.can_process(self.statement):
                self.task.domain = self.domain_adapter.process(self.statement)

        if not self.task.intent:
            intent_adapter = CustomIntentAdapter(
                self.task.domain,
                trainer=self.kwargs.get('intent_trainer'),
                storage=self.storage
            )

            if intent_adapter.can_process(self.statement):
                self.task.intent = intent_adapter.process(self.statement)
            else:
                # special process for scenario if we cannot process
                pass

        if self.task.intent:
            prm_adapter = CustomSlotFillingAdapter(
                self.task.intent,
                self.task.parameters,
                storage=self.storage
            )

            if prm_adapter.can_process(self.statement):
                self.task.parameters = prm_adapter.process(self.statement)
            else:
                # another special scenario if we cannot process it
                pass

        return self.task