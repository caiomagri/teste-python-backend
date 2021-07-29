from .models import Bet
from rest_framework import serializers


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ['id', 'user', 'numbers', 'created_at']
        read_only_fields = ['id']
