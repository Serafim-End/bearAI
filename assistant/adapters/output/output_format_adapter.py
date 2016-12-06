# coding: utf-8

import json

from assistant.adapters.output.output_adapter import OutputAdapter


class OutputFormatAdapter(OutputAdapter):

    JSON = 'json'

    VALID_FORMATS = (JSON, )

    def __init__(self, **kwargs):
        super(OutputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('format')

        if not self.format:
            self.format = self.JSON

        if self.format not in self.VALID_FORMATS:
            raise self.UnrecognizedOutputFormatException()

    def process_response(self, response):
        """
        :param response: should be serializable
        :return: json object
        """
        return json.dumps(response)

    class UnrecognizedOutputFormatException(Exception):
        def __init__(self, value='format not recognized.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
