# coding: utf-8

from assistant.trainer import Trainer


class IntentTrainer(Trainer):
    """
    main goal is to detect intent from statement
    """

    def __init__(self, storage, **kwargs):

        self.storage = storage

        super(IntentTrainer, self).__init__(self.storage, **kwargs)

    def train(self):
        raise NotImplementedError()
