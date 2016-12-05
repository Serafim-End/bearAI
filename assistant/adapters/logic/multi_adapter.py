# coding: utf-8

from logic_adapter import LogicAdapter


class MultiLogicAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        self.adapters = []

    def process(self, statement):

        result = None
        max_confidence = -1

        for adapter in self.adapters:
            if adapter.can_process(statement):
                confidence, output = adapter.process(statement)

                if confidence > max_confidence:
                    result = output
                    max_confidence = confidence

        return max_confidence, result

    def add_adapter(self, adapter, order_index=None):
        if not order_index:
            self.adapters.append(adapter)
        else:
            self.adapters.insert(order_index, adapter)

    def set_context(self, context):
        super(MultiLogicAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)
