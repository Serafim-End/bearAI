# coding: utf-8

import pandas as pd

from assistant.assistant import Assistant
from assistant.utils.w2v_processing import (
    w2v_transformation,  get_word2vec_model
)
from intent.adapter import IntentAdapter
from intent.models import Intent
from intent.trainer import IntentTrainer


class CustomIntentAdapter(IntentAdapter):
    def __init__(self, domain, **kwargs):
        super(CustomIntentAdapter, self).__init__(domain, **kwargs)

        self.trainer = kwargs.get('trainer')
        if not self.trainer:
            self.trainer = CustomIntentTrainer(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):
        data = self.trainer.preprocess_message(statement.message)
        pred_intent_id = self.trainer.clf.predict(data)
        return pred_intent_id[0]
        # return Intent.objects.filter(id=pred_intent_id).first()


class CustomIntentTrainer(IntentTrainer):

    def __init__(self, storage, **kwargs):
        self.storage = storage

        assistant = Assistant()
        self.clf = assistant.domain_trainer
        self.word2vec_model = None

        self.word2vec_filename = kwargs.get('word2vec_filename')
        self.data_filename = kwargs.get('data_filename')

        super(CustomIntentTrainer, self).__init__(
            self.storage, **kwargs
        )

        if self.data_filename:
            self.data = pd.read_csv(self.data_filename)

    def train(self):
        """
        train the model from sources
        but clearly it should be saved in file
        :return:
        """
        pass

    def create_model(self):
        """
        It is simple variant of the model - baseline
        :return:
        """
        pass

    def preprocess_message(self, message):
        if not self.word2vec_filename:
            raise Exception('cannot find word2vec file with model')

        if not self.word2vec_model:
            self.word2vec_model = get_word2vec_model(
                self.word2vec_filename,
                binary=True
            )

        if not self.word2vec_model:
            raise Exception('cannot find word2vec model')

        w2v_data, _ = w2v_transformation([message], [0], self.word2vec_model)
        return w2v_data
