# coding: utf-8

from assistant.trainer import Trainer


class SlotFillingTrainer(Trainer):
    """
    main goal is to detect parameters from statement
    """

    def __init__(self, storage, **kwargs):

        self.storage = storage

        super(SlotFillingTrainer, self).__init__(self.storage, **kwargs)

    def train(self):
        raise NotImplementedError()
