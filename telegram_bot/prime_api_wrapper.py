# coding: utf-8


def reserve_request_parameters(persons_count, datetime_par, restaurant_id):
    parameters_dict = {
        "taskTypeId": 9,
        "comment": "Задача заведена через API из телеграм бота",
        "restaurant": {
            "personsCount": persons_count,
            "datetime": datetime_par,
            "restaurantId": restaurant_id
        }
    }
    return  parameters_dict
