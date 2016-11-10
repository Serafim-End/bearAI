# coding: utf-8

from assistant.trainer import Trainer


class DomainTrainer(Trainer):
    """
    used in DomainAdapter - domain/adapter
    """
    def __init__(self, storage, **kwargs):

        self.storage = storage

        super(DomainTrainer, self).__init__(self.storage, **kwargs)

    def train(self):
        raise NotImplementedError()
