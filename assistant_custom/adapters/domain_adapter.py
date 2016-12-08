# coding: utf-8

import pandas as pd

from sklearn.ensemble import BaggingClassifier

from assistant.assistant import Assistant
from assistant.utils.module_loading import import_loading
from assistant.utils.w2v_processing import (
    w2v_transformation,
    get_word2vec_model
)
from domain.adapter import DomainAdapter
from domain.models import Domain
from domain.models import DomainData
from domain.trainer import DomainTrainer


class CustomDomainAdapter(DomainAdapter):

    def __init__(self, **kwargs):
        super(CustomDomainAdapter, self).__init__(**kwargs)

        # we should specify a lot of additional parameters
        self.trainer = kwargs.get('trainer')
        if not self.trainer:
            self.trainer = CustomDomainTrainer(
                **kwargs
            )

    def can_process(self, statement):
        """
        i thought that initialization of any models should be here
        but word2vec model may be in another place - it is really huge
        :param statement:
        :return:
        """
        if statement:
            return True
        return False

    def process(self, statement):
        """
        predict for domain class should be here
        :param statement: message from the user
        :return:
        """
        data = self.trainer.preprocess_message(statement.message)
        domain_cls = self.trainer.clf.predict(data)
        return domain_cls[0]
        # return Domain.objects.filter(id=domain_cls).first()


class CustomDomainTrainer(DomainTrainer):

    def __init__(self,  **kwargs):
        self.storage = kwargs.get('storage')
        super(CustomDomainTrainer, self).__init__(**kwargs)

        assistant = Assistant()
        self.clf = assistant.domain_trainer
        self.word2vec_model = None

        self.word2vec_filename = kwargs.get('word2vec_filename')
        self.data_filename = kwargs.get('data_filename')
        if self.data_filename:
            self.data = pd.read_csv(self.data_filename)

    def train(self):
        """
        train the model from sources
        but clearly it should be saved in file
        :return:
        """

        if self.clf is None:
            self.create_model()

        self.clf.fit(self.data)

    def create_model(self):
        """
        It is simple variant of the model - baseline
        :return:
        """

        self.clf = BaggingClassifier(n_estimators=100)

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
