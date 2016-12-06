# coding: utf-8


class ContextManager(object):

    def __init__(self, statement, task, **kwargs):
        self.statement = statement
        self.task = task

    def process_task(self):
        raise NotImplementedError()
