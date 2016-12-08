# coding: utf-8

from django.http import JsonResponse
from rest_framework import views

from agent.models import Agent

from assistant.assistant import Assistant
from customer.models import Customer
from developer.models import Developer


class TelegramBotView(views.APIView):

    def add_new_user(self, telegram_user_id):

        dev = Developer(account_status='LOW')
        dev.save()

        agent = Agent(developer=dev, username='michael')
        agent.save()

        customer = Customer(agent=agent, username=telegram_user_id)
        customer.save()
        return customer

    def get(self, request, *args, **kwargs):

        telegram_user_id = 1
        message_default = 'забронировать ресторан Воронеж на завтра у окна'.decode('utf-8')

        customer = Customer.objects.filter(username=telegram_user_id).last()
        if not customer:
            customer = self.add_new_user(telegram_user_id)

        assistant_instance = Assistant(
            input_class='assistant_custom.adapters.input_adapter.CustomInputAdapter',
            storage_class='assistant.adapters.storage.storage_adapter.StorageAdapter',
            output_class='assistant.adapters.output.output_format_adapter.OutputFormatAdapter',
            context_manager='assistant_custom.context_manager.CustomContextManager',
            customer=customer,
        )

        message = request.GET.get('message', message_default)
        return JsonResponse(assistant_instance.response(message))