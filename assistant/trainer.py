from conversation.models import Statement, Response
from corpus.corpus import Corpus


class Trainer(object):

    def __init__(self, storage, **kwargs):
        """
        :param storage: if it is not useless
        :param kwargs: for any prms
        :return:
        """
        self.storage = storage
        self.corpus = Corpus()

    def train(self, *args, **kwargs):
        raise self.TrainerInitializationException()

    class TrainerInitializationException(Exception):

        def __init__(self, value=None):
            default = 'A training class must be specified'
            self.value = value or default

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        result = []

        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result


class ListTrainer(Trainer):

    def get_or_create(self, statement_text):
        statement = self.storage.find(statement_text)
        if not statement:
            statement = Statement(statement_text)

        return statement

    def train(self, conversation):
        statement_history = []

        for text in conversation:
            statement = self.get_or_create(text)

            if statement_history:
                statement.add_response(
                    Response(statement_history[-1].text)
                )

            statement_history.append(statement)
            self.storage.update(statement, force=True)


class AssistantCorpusTrainer(Trainer):

    def train(self, *corpora):
        trainer = ListTrainer(self.storage)

        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    trainer.train(pair)
