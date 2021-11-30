from rest_framework import serializers

from src.oauth import models
from src.tickets import models as tickets_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('id', 'email', 'miles',)


class GoogleAuth(serializers.Serializer):
    """Серилизация почты/пароля"""
    email = serializers.EmailField()
    token = serializers.CharField()


class MailPasswordAuth(serializers.Serializer):
    """Серилизация данных почты/пароль"""
    email = serializers.EmailField()
    password = serializers.CharField()


class MailAcceptCode(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()


