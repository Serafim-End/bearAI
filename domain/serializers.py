from rest_framework import serializers

from domain.models import Domain


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = ('__all__')
