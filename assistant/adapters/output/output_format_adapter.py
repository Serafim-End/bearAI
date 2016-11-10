# coding: utf-8

from assistant.adapters.output.output_adapter import OutputAdapter


class OutputFormatAdapter(OutputAdapter):

    JSON = 'json'
    TEXT = 'text'
    OBJECT = 'object'

    VALID_FORMATS = (JSON, TEXT, OBJECT, )

    def __init__(self, *args, **kwargs):
        super(OutputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('output_format', 'object')

        if self.format not in self.VALID_FORMATS:
            raise self.UnrecognizedOutputFormatException()

    def process_response(self, statement, confidence=None):
        if self.format == self.TEXT:
            return statement.text

        if self.format == self.JSON:
            return statement.serialize()
        return statement

    class UnrecognizedOutputFormatException(Exception):
        def __init__(self, value='format not recognized.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
