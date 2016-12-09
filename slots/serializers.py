# coding: utf-8

from rest_framework import serializers

from slots.models import Parameter


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('intent', 'is_obligatory', 'name', 'value')
