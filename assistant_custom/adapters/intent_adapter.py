# coding: utf-8

from intent.adapter import IntentAdapter


class CustomIntentAdapter(IntentAdapter):
    def __init__(self, domain, **kwargs):
        super(CustomIntentAdapter, self).__init__(domain, **kwargs)

        self.trainer = kwargs.get('trainer')

    def can_process(self, statement):
        return True

    def process(self, statement):
        raise self.AdapterMethodNotImplemented()
