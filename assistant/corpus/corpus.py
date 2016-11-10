# coding: utf-8


class CorpusInterface(object):
    def load_corpus(self, corpus):
        pass

    def read_corpus(self, filename):
        pass


class Corpus(object):
    def load_corpus(self, corpus):
        raise NotImplementedError()

    def read_corpus(self, filename):
        raise NotImplementedError()
