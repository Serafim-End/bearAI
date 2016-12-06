# coding: utf-8

import pandas as pd
import numpy as np

import gensim
import pymorphy2

from sklearn.ensemble import BaggingClassifier

from domain.adapter import DomainAdapter
from domain.trainer import DomainTrainer


class CustomDomainAdapter(DomainAdapter):

    def __init__(self, **kwargs):
        super(CustomDomainAdapter, self).__init__(**kwargs)

        # we should specify a lot of additional parameters
        self.trainer = kwargs.get('trainer')
        if not self.trainer:
            self.trainer = CustomDomainTrainer(self.storage, **kwargs)

    def can_process(self, statement):
        """
        i thought that initialization of any models should be here
        but word2vec model may be in another place - it is really huge
        :param statement:
        :return:
        """
        self.trainer.word2vec_model = self.trainer.get_word2vec_model(
            self.trainer.word2vec_filename,
            binary=True
        )

        return True

    def process(self, statement):
        """
        predict for domain class should be here
        :param statement: message from the user
        :return:
        """
        data = self.trainer.preprocess_message(statement.message)
        return self.trainer.clf.predict(data)

    def update_domain_data(self, can_update):
        """
        obvious that some stuff with storage should be here
        :param can_update:  boolean value that shows that
        you have already gone through the customer and that domain is correct
        :return: boolean that illustrates the status of db updates
        """
        pass


class CustomDomainTrainer(DomainTrainer):

    def __init__(self, storage, **kwargs):
        self.storage = storage
        super(CustomDomainTrainer, self).__init__(self.storage, **kwargs)

        self.clf = None
        self.word2vec_model = None

        self.morph = pymorphy2.MorphAnalyzer()
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
            self.word2vec_model = self.get_word2vec_model(
                self.word2vec_filename,
                binary=True
            )

        if not self.word2vec_model:
            raise Exception('cannot find word2vec model')

        w2v_data, _ = self.w2v_transformation([message], [0])
        return w2v_data

    def get_word2vec_model(self, binary_filename, **kwargs):
        """
        get word2vec model from source file
        it is impossible to learn it here

        :param binary_filename: filename (binary format)
        :param kwargs: it is really binary (binary=True)
        :return: word2vec model
        """
        model = gensim.models.Word2Vec.load_word2vec_format(
            binary_filename,
            binary=kwargs.get('binary')
        )

        model.init_sims(replace=True)
        return model

    def w2v_transformation(self, data, labels):
        """
        transform the data - it can be pandas format or just array
        labels for indexing because not all rows can be transformed
        :param data: data - pandas, numpy, list
        :param labels: pandas, numpy, list
        :return: transformed_data and appropriate labels
        """

        mapping = {
            'ADJF': '_A',
            'NOUN': '_S',
            'INFN': '_V',
        }

        train_vectors = []
        train_labels = []
        # save indexes of labels
        for i, s in enumerate(data):
            words = s.split(' ')

            words_vector = None
            words_count = 0

            for w in words:
                w = self.morph.parse(w)[0]
                if w.tag.POS in mapping:
                    new_w = '{}{}'.decode('utf-8').format(w.normal_form,
                                                          mapping[w.tag.POS])
                    v = self.vector(new_w)
                    if isinstance(v, np.ndarray):
                        words_count += 1

                        if isinstance(words_vector, np.ndarray):
                            words_vector = words_vector + v

            if isinstance(words_vector, np.ndarray) and words_count > 0:
                words_vector = words_vector / words_count
            else:
                words_vector = None

            if isinstance(words_vector, np.ndarray):
                train_labels.append(labels[i])
                train_vectors.append(words_vector)

        train_vectors = np.array(train_vectors)
        return train_vectors, np.array(train_labels)

    def vector(self, q):
        """
        transform a single word to word2vec model - 500 digits
        :param q: just a word from w2v vocabulary
        :return: vector from 500 digits, numpy
        """
        qf = q

        if q not in self.word2vec_model:
            candidates_set = set()

            candidates_set.add(q.upper())
            candidates_set.add(q.lower())
            candidates_set.add(q.capitalize())

            no_results = True
            for candidate in candidates_set:
                if candidate in self.word2vec_model:
                    qf = candidate
                    no_results = False
                    break

            if no_results:
                # obvious that not all elements
                # in corpus will from our vocabulary
                return None

        raw_vector = self.word2vec_model[qf]
        return raw_vector
