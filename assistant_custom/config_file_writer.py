# coding:utf-8
# flake8: noqa
import json

my_config = {
    'domain': [
        {
            'name': 'Рестораны',
            'intent': [
                {
                    'name': 'Бронирование',
                    'parameters': [
                        {
                            'name': 'personsCount',
                            'is_obligatory': True,
                            'value': 'integer',
                        },

                        {
                            'name': 'datetime',
                            'is_obligatory': True,
                            'value': 'time',
                        },

                        {
                            'name': 'restName',
                            'is_obligatory': True,
                            'value': json.dumps(
                                {
                                    'воронеж': ('ворож', 'ворожня'),
                                    'erwin': ('ервин', 'эрвин')
                                }
                            ),
                        },

                        {
                            'name': 'location',
                            'is_obligatory': False,
                            'value': json.dumps({}),
                        }
                    ]
                }
            ]
        }
    ]
}

with open('prime.config', 'w') as outfile:
    json.dump(my_config, outfile)

