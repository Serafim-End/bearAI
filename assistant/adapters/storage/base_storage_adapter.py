# coding: utf-8
# flake8: noqa

from ..adapter import Adapter

from developer.models import Developer
from agent.serializers import AgentSerializer
from domain.models import Domain
from domain.serializers import DomainSerializer
from slots.serializers import ParameterSerializer
from intent.serializers import IntentSerializer
from intent.models import Intent
from intent.models import IntentData
from intent.serializers import IntentDataSerializer


class BaseStorageAdapter(Adapter):

    def get_class(self, cls):
        if isinstance(cls, str):
            cls = globals()[cls]
        return cls

    def func_object(self, cls, func_names, **kwargs):
        cls = self.get_class(cls)

        f = reduce(lambda c, e: getattr(c, e), func_names, cls)

        return f(**kwargs)

    class SerializerException(Exception):

        def __init__(self, msg):
            self.msg = msg
            raise Exception(msg) if msg else 'Serializer error'
