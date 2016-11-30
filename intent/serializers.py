from rest_framework import serializers

from intent.models import Intent, IntentData


class IntentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Intent
        fields = ('domain', 'date_joined', 'name')


class IntentDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntentData
        fields = ('intent', 'text')
