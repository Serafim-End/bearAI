# coding:utf-8
# flake8: noqa

import json

from input_adapter import InputDevAdapter

from assistant.adapters.storage.storage_adapter import StorageAdapter


class CRMAdapter(InputDevAdapter):

    def __init__(self, file_path):
        super(CRMAdapter, self).__init__()

        self.file_path = file_path
        self.storage_adapter = StorageAdapter()

    def process_input(self, **kwargs):

        agent_name = kwargs.get('agent_name')

        with open(self.file_path) as data_file:
            data = json.load(data_file)

        developer, created = self.storage_adapter.func_object(
            'Developer', ['objects', 'get_or_create']
        )

        agent = self.storage_adapter.save(
            'AgentSerializer',
            data={
                'developer': developer.pk,
                'username': agent_name if agent_name else 'username'
            }
        )

        for domain in data['domain']:
            domain_ser = self.storage_adapter.get_object(
                'Domain', name=domain['name']
            )
            if not domain_ser:
                domain_ser = self.storage_adapter.save(
                    'DomainSerializer',
                    data={'agent': agent.pk, 'name': domain['name']}
                )

            for intent in domain['intent']:
                intent_ser = self.storage_adapter.get_object(
                    'Intent', name=intent['name']
                )

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
