from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models as models_app
from src.oauth.models import AuthUser
from src.oauth.serializers import UserSerializer
from django.db import models
# Create your views here.
from .serializers import TicketSerializer, FlightSerializer


class UsersTickets(generics.ListAPIView):
    """Список билетов купленных пользователем"""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer_serialized = UserSerializer(self.request.user)
        print(customer_serialized.data)

        tickets = models_app.Ticket.objects.filter(Customer__id=customer_serialized.data['id'])

        return tickets