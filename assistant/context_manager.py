# coding: utf-8


class ContextManager(object):

    def __init__(self, statement):
        self._statement = statement
        self.status = self.detect_task_status()

    def detect_task_status(self):
        raise NotImplementedError()
