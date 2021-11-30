from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

from .. import serializers
from ..services.google import check_google_auth
from ..services.mail_auth import check_mail_password_auth, check_mail_password_reg, accept_user


def google_login(request):
    return render(request, 'oauth/google_login.html')


@api_view(['POST'])
def google_auth(request):
    """Подтверждение авторизации гугл"""
    google_data = serializers.GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data Google')


@api_view(['POST'])
def mail_auth(request):
    """Авторизация через почту/пароль"""
    user_data = serializers.MailPasswordAuth(data=request.data)
    if user_data.is_valid():
        token = check_mail_password_auth(user_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data mail/password')


@api_view(['POST'])
def mail_reg(request):
    """Регистрация через почту/пароль"""
    user_data = serializers.MailPasswordAuth(data=request.data)
    if user_data.is_valid():
        token = check_mail_password_reg(user_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data mail/password')


@api_view(['POST'])
def mail_accept(request):
    """Подтверждение пользователя"""
    user_data = serializers.MailAcceptCode(data=request.data)
    if user_data.is_valid():
        token = accept_user(user_data.data)
        return Response(token)
    else:
        raise AuthenticationFailed(code=403, detail='Bad data mail')



