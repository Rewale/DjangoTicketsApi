from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed

from src.oauth import serializers

from src.oauth.models import AuthUser
from . import base_auth


def check_mail_password_auth(user_data: serializers.MailPasswordAuth) -> dict:
    """Авторизация через почту
    TODO:Добавить подтверждение почты через код"""
    try:
        user = AuthUser.objects.get(email=user_data['email'], password=user_data['password'])
    except AuthUser.DoesNotExist:
        raise AuthenticationFailed(code=403,
                                   detail='Неверный адрес почты/пароль')
    except:
        raise AuthenticationFailed(code=403,
                                   detail='Неверный адрес почты/пароль')

    return base_auth.create_token(user.id)


def check_mail_password_reg(user_data: serializers.MailPasswordAuth) -> dict:
    """Регистрация через почту
    TODO:Добавить подтверждение почты через код"""
    try:
        user = AuthUser.objects.create(email=user_data['email'], password=user_data['password'])
    except IntegrityError:
        raise AuthenticationFailed(code=403,
                                   detail='Такой пользователь уже существует')

    return base_auth.create_token(user.id)


