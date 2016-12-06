# coding: utf-8

from slots.adapter import SlotFillingAdapter


class CustomSlotFillingAdapter(SlotFillingAdapter):
    def __init__(self, intent, parameters, **kwargs):
        super(CustomSlotFillingAdapter, self).__init__(intent, **kwargs)

        self.parameters = parameters

    def can_process(self, statement):
        return True

    def process(self, statement):
        raise self.AdapterMethodNotImplemented()
