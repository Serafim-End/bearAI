# coding: utf-8

from rest_framework import serializers

from models import Session


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = ('domain', 'intent', 'parameters',
                  'is_obligatory', 'date_joined')
