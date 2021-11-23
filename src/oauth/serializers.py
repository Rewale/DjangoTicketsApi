from rest_framework import serializers

from src.oauth import models
from src.tickets import models as tickets_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('id', 'email', 'miles',)


class GoogleAuth(serializers.Serializer):
    """Серилизация данных от гугл"""
    email = serializers.EmailField()
    token = serializers.CharField()


class MailPasswordAuth(serializers.Serializer):
    """Серилизация данных от гугл"""
    email = serializers.EmailField()
    password = serializers.CharField()


