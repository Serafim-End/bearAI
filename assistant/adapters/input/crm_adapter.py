# coding:utf-8
# flake8: noqa

import json

from domain.models import Domain
from input_adapter import InputDevAdapter

from assistant.adapters.storage.storage_adapter import StorageAdapter
from intent.models import Intent


class CRMAdapter(InputDevAdapter):

    def __init__(self, file_path):
        super(CRMAdapter, self).__init__()

        self.file_path = file_path
        self.storage_adapter = StorageAdapter()

    def load_json_file(self):
        with open(self.file_path) as data_file:
            return json.load(data_file)

    def process_input(self):
        data = self.load_json_file()

        developer, created = self.storage_adapter.func_object(
            'Developer', ['objects', 'get_or_create']
        )

        agent = self.storage_adapter.save(
            'AgentSerializer',
            data={'developer': developer.pk, 'username': 'michaelborisov'}
        )

        for domain in data['domain']:
            domain_ser = Domain.objects.filter(name=domain['name']).first()
            if not domain_ser:
                domain_ser = self.storage_adapter.save(
                    'DomainSerializer',
                    data={'agent': agent.pk, 'name': domain['name']}
                )

            for intent in domain['intent']:
                intent_ser = Intent.objects.filter(name=intent['name']).first()
                if not intent_ser:
                    intent_ser = self.storage_adapter.save(
                        'IntentSerializer',
                        data={'domain': domain_ser.pk, 'name': intent['name']}
                    )

                for parameter in intent['parameters']:
                    self.storage_adapter.save(
                        'ParameterSerializer',
                        data={
                            'intent': intent_ser.pk,
                            'name': parameter['name'],
                            'is_obligatory': bool(parameter['is_obligatory']),
                            'value': parameter['value']
                        }
                    )
