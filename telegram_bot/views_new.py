# coding: utf-8
import urllib
from datetime import datetime
import telepot
from django.http import JsonResponse
from django.http.response import HttpResponse
from rest_framework import views
from telepot.namedtuple import InlineKeyboardMarkup

from agent.models import Agent

from assistant.assistant import Assistant
from customer.models import Customer
from developer.models import Developer
from telegram_bot.navigator_api_parser import load_navigator_api
from telegram_bot.settings import (
    TELEGRAM_BOT_TOKEN, NAVIGATOR_SEARCH_LINK,
    NAVIGATOR_TOKEN
)


class AssistantWrapper(object):
    assistance_instance = None

    @staticmethod
    def initialize_assistant(customer):
        AssistantWrapper.assistance_instance = Assistant(
            input_class='assistant_custom.adapters.input_adapter.CustomInputAdapter',
            storage_class='assistant.adapters.storage.storage_adapter.StorageAdapter',
            output_class='assistant.adapters.output.output_format_adapter.OutputFormatAdapter',
            context_manager='assistant_custom.context_manager.CustomContextManager',
            customer=customer,
        )


class TelegramBotView(views.APIView):

    def add_new_user(self, telegram_user_id):

        dev = Developer(account_status='LOW')
        dev.save()

        agent = Agent(developer=dev, username='michael')
        agent.save()

        customer = Customer(agent=agent, username=telegram_user_id)
        customer.save()
        return customer

    def process_bear(self, message, telegram_user_id):

        customer = Customer.objects.filter(username=telegram_user_id).last()
        if not customer:
            customer = self.add_new_user(telegram_user_id)

        if not AssistantWrapper.assistance_instance:
            AssistantWrapper.initialize_assistant(customer)

        assistant_instance = AssistantWrapper.assistance_instance

        return assistant_instance.response(message)

    def get(self, request, *args, **kwargs):

        telegram_user_id = 72772783
        message_default = (
            'забронировать ресторан Воронеж на завтра у окна'
        ).decode('utf-8')
        message = request.GET.get('message', message_default)

        # in this place can be another function, but with the same structure

        response = self.process_bear(
            message=message,
            telegram_user_id=telegram_user_id
        )

        # further (in continuous development)
        #  please process structure like serialized task object
        return JsonResponse(response)

    def post(self, request, *args, **kwargs):
        payload = request.data
        bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
        if 'message' in payload:
            tuid = payload['message']['from']['id']
            customer = Customer.objects.filter(username=tuid).last()

            if not customer:
                customer = self.add_new_user(tuid)
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')

            response = self.process_bear(
                message=cmd,
                telegram_user_id=tuid
            )

            rest_name = ''
            persons_count = ''
            datetime_par = ''
            for parameter in response['parameter']:
                if parameter['name'] == 'restName':
                    rest_name = parameter.get('value', '')

                if parameter['name'] == 'personsCount':
                    persons_count = parameter.get('value', '')

                if parameter['name'] == 'datetime':
                    datetime_par = parameter.get('value', '')

            rest_name = urllib.quote_plus(rest_name.encode('utf-8'))

            info = load_navigator_api(
                NAVIGATOR_SEARCH_LINK.format(
                    NAVIGATOR_TOKEN,
                    rest_name
                )
            )
            if info['poster']:
                bot.sendPhoto(chat_id, info['poster'])
            if info['address']:
                bot.sendMessage(chat_id, info['address'])
            if info['location']:
                bot.sendLocation(
                    chat_id,
                    info['location']['lat'],
                    info['location']['lng'],
                )
            if info['description']:

                my_day = datetime.strptime(
                    datetime_par, '%Y-%m-%dT%H:%M:%S.%f'
                )
                markup = InlineKeyboardMarkup(inline_keyboard=[[
                    dict(text='Сайт', url=info.get('web_site')),
                    dict(text='Забронировать',
                         callback_data='r{}p{}d{}'.format(
                             info.get('crm_id', ''),
                             persons_count,
                             '{}+{}'.format(
                                 my_day.strftime('%Y%m%d%H%M'), '0200'
                             )
                         ))
                ]])

                bot.sendMessage(
                    chat_id=chat_id,
                    text=info['description'],
                    reply_markup=markup
                )
            else:
                bot.sendMessage(chat_id=chat_id, text='Oops')

        if 'callback_query' in payload:
            cmd = payload['callback_query']['data']
            chat_id = payload['callback_query']['message']['chat']['id']
            tuid = payload['callback_query']['message']['from']['id']

            r_ind = cmd.index('r')
            p_ind = cmd.index('p')
            d_ind = cmd.index('d')
            restaurant_id = cmd[r_ind + 1: p_ind]
            persons_count = cmd[p_ind + 1: d_ind]
            datetime_par = cmd[d_ind+1: len(cmd)]

            if (restaurant_id and
                    persons_count and
                    datetime_par):
                bot.sendMessage(chat_id, 'Обращаемся к API')
            else:
                if not persons_count:
                    bot.sendMessage(
                        chat_id, 'Пожалуйста, укажите количество гостей'
                    )


        return HttpResponse('Successfully echoed')
