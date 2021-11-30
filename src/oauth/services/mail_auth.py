import random

from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed

from src.oauth import serializers

from src.oauth.models import AuthUser
from . import base_auth


def check_mail_password_auth(user_data: serializers.MailPasswordAuth) -> dict:
    """Авторизация через почту
    """

    try:
        user = AuthUser.objects.get(email=user_data['email'], password=user_data['password'])
        print(user.accept_code)
        if user.accept_code is not None:
            raise AuthenticationFailed(code=403,
                                       detail='Подтвердите учетную запись')
    except AuthUser.DoesNotExist:
        raise AuthenticationFailed(code=403,
                                   detail='Неверный адрес почты/пароль')

    return base_auth.create_token(user.id)


def check_mail_password_reg(user_data: serializers.MailPasswordAuth) -> str:
    """Регистрация через почту"""
    try:
        user = AuthUser.objects.create(email=user_data['email'], password=user_data['password'],
                                       accept_code=random.randint(10000, 50000))
        from django.core.mail import send_mail

        send_mail(
            'Code',
            str(user.accept_code),
            None,
            [user.email],
            fail_silently=False,
        )
    except IntegrityError:
        raise AuthenticationFailed(code=403,
                                   detail='Такой пользователь уже существует')

    return "Для продолжения подтвердите учетную запись"


def accept_user(user_data: serializers.MailAcceptCode) -> dict:
    """Подтверждние учетной записи"""
    try:
        user = AuthUser.objects.get(email=user_data['email'])
        if user.accept_code == user_data['code']:
            user.accept_code = None
            user.save()
            return base_auth.create_token(user.id)
        else:
            raise AuthenticationFailed(code=403,
                                       detail='Неверный код подтверждения')
    except AuthUser.DoesNotExist:
        raise AuthenticationFailed(code=403,
                                   detail='Неверный адрес почты/пароль')
