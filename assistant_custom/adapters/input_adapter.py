# coding: utf-8

from assistant.utils.w2v_processing import morph
from assistant.adapters.input.input_adapter import InputAdapter
from assistant.conversation.models import Statement
from customer.models import Customer


class CustomInputAdapter(InputAdapter):
    def __init__(self, **kwargs):
        super(CustomInputAdapter, self).__init__()

        self.storage = kwargs.get('storage')

    def process_input(self, input_sequence, customer, **kwargs):
        """
        process the input, filter it
        :param input_sequence:
        :param kwargs:
        :return:
        """

        if not isinstance(input_sequence, (str, unicode)):
            raise self.InputAdapterError()

        customer = Customer.objects.get_or_create(id=customer.id)

        # text processing

        message = ' '.join(
            [
                morph.parse(w)[0].normal_form
                for w in input_sequence.split(' ') if not w.isdigit()
            ]
        )

        return Statement(customer=customer, message=message)



