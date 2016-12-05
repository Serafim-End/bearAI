# coding: utf-8


class ContextManager(object):

    def __init__(self, statement, task):
        self.statement = statement
        self.task = task

    def create_new_task(self):
        raise NotImplementedError()
