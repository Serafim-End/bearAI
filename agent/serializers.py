from rest_framework import serializers

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = ('developer', 'username', 'date_joined')
