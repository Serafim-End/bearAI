# flake8: noqa
# coding: utf-8
import contextlib
import json
import ssl
import urllib
import urllib2

import telepot
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework import views

from agent.models import Agent
from assistant.adapters.input.crm_adapter import CRMAdapter
from assistant.adapters.storage.storage_adapter import StorageAdapter
from assistant.assistant import Assistant
from assistant.conversation.models import Statement
from assistant_custom.context_manager import CustomContextManager
from customer.models import Customer
from developer.models import Developer
from intent.models import Intent
from session.models import CustomerSession, Session
from slots.models import Parameter
from telegram_bot.settings import (
    PRIME_APIKEY, TELEGRAM_BOT_TOKEN,
    RESTAURANT_API_URL
)


class TelegramBotView(views.APIView):
    def proceed_message(self, message, parameter):
        if parameter in message:
            return message
        return ''

    def add_new_user(self, tuid):
        dev = Developer.objects.last()
        agent = Agent(developer=dev, username='michael')
        agent.save()
        customer = Customer(agent=agent, username=tuid)
        customer.save()
        return customer

    def proceed_message_inside_session(self, message):

        customer = Customer.objects.filter(
            email='michaelborisovha@gmail.com'
        ).first()

        customer_session = customer.session_set.last()
        if not customer_session.session.is_active:
            session = Session(
                intent=Intent.objects.filter(name='Бронирование').first(),
                is_active=True
            )
            session.load_parameters()
            session.save()

            customer_session.save()

        parameters = json.loads(customer_session.session.parameters)
        for i_parameter in xrange(len(parameters)):
            for k, v in parameters[i_parameter].iteritems():
                if k == 'is_obligatory':
                    continue
                if not v:
                    parameters[i_parameter][k] = self.proceed_message(
                        message, k
                    )
        customer_session.session.parameters = json.dumps(parameters)
        customer_session.session.save()

        unknown_pars = []
        for parameter in parameters:
            for k, v in parameter.iteritems():
                if k == 'is_obligatory':
                    continue
                if not v and parameter.get('is_obligatory'):
                    unknown_pars.append(k)
        if len(unknown_pars) != 0:
            unknown_str = ', '.join(unknown_pars)
            return 'I dont know the following parameters: {}'.format(
                unknown_str)

        else:
            customer_session.session.is_active = False
            customer_session.session.save()
            return 'Session is closed'

    def detect_domain(self, message):
        pass

    def detect_intent(self, message):
        pass

    def load_data_api(self, url):
        context = ssl._create_unverified_context()
        request = urllib2.Request(
            url,
            headers={"Authorization": PRIME_APIKEY,
                     "Content-Type": "application/json"}
        )

        with contextlib.closing(
                urllib2.urlopen(request, context=context)) as jf:
            d = json.loads(jf.read())
            if 'data' in d and len(d['data']):
                return d['data'][0]  # наиболее вероятный
            else:
                return None

    def get(self, request, *args, **kwargs):
        message = request.GET.get('message', '')
        #self.proceed_message_inside_session(message)
        tuid = 72772783  # payload['message']['from']['id']
        customer = Customer.objects.filter(username=tuid).last()
        if not customer:
            customer = self.add_new_user(tuid)
        # if not customer:
        #     customer = self.add_new_user(tuid)
        # # chat_id = payload['message']['chat']['id']
        # cmd = message # payload['message'].get('text')
        assistant_instance = Assistant(
            input_class='assistant_custom.adapters.input_adapter.CustomInputAdapter',
            storage_class='assistant.adapters.storage.storage_adapter.StorageAdapter',
            output_class='assistant.adapters.output.output_format_adapter.OutputFormatAdapter',
            context_manager='assistant_custom.context_manager.CustomContextManager',
            customer=customer,
        )

        message = request.GET.get('message')
        # message = 'забронируйте столик в erwin'.decode('utf-8')
        return HttpResponse(assistant_instance.response(message))
        # Parameter.objects.all().delete()
        # adapter = CRMAdapter('/Users/michaelborisov/Desktop/another_bot/bot/assistant_custom/prime.config')
        # adapter.process_input()


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
            # statement = Statement(
            #     customer=customer, message='Hello from the other side'
            # )
            # statement.save()
            task = StorageAdapter().get_task(customer)
            ccm = CustomContextManager(
                cmd, task, status='True', word2vec_filename='/Users/michaelborisov/Desktop/bot/templates/word2vec_trainer'
            )
            res = ccm.process_task()
            f = {'q': cmd.encode('utf-8')}
            r = urllib.urlencode(f)
            message = self.proceed_message_inside_session(cmd)
            data_api = self.load_data_api(RESTAURANT_API_URL.format(r))
            if data_api:
                bot.sendMessage(chat_id=chat_id, text=data_api['name'])
            else:
                bot.sendMessage(chat_id=chat_id, text=message)

        return HttpResponse('Successfully echoed')
