from rest_framework import generics, permissions
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from src.oauth.serializers import UserSerializer
from . import models as models_app
# Create your views here.
from .filters import FlightFilter
from .serializers import TicketDetailSerializer, FlightSerializer, TicketBuySerializer


# TODO Доступ к конкретному билету по ссылке


class UsersTickets(generics.ListAPIView):
    """Список билетов купленных пользователем"""
    serializer_class = TicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer_serialized = UserSerializer(self.request.user)
        # print(customer_serialized.data)

        tickets = models_app.Ticket.objects.filter(customer__id=customer_serialized.data['id'])

        return tickets


class TicketsListView(generics.ListAPIView):
    """Вывод списка билетов"""
    serializer_class = TicketDetailSerializer

    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = service.MovieFilter
    # permission_classes = [permissions.IsAuthenticated]

    # Не выводим купленные билеты
    def get_queryset(self):
        tickets = models_app.Ticket.objects.filter(customer=None)

        return tickets


class TicketsDetailView(APIView):
    """Вывод билета определенного рейса"""

    def get(self, request, flight_num, seq):
        ticket = models_app.Ticket.objects.get(pk=seq, flightOfTicket=flight_num)
        serializer = TicketDetailSerializer(ticket)

        return Response(serializer.data)


class FlightListView(generics.ListAPIView):
    # TODO: Количетсво билетов которые НЕ купили
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        flights = models_app.Flight.objects.annotate(count_tickets=models.Count('tickets'))

        return flights


class FlightDetailView(APIView):

    def get(self, request, flight_num):
        try:
            flight = models_app.Flight.objects.annotate(count_tickets=models.Count('tickets')).get(flight_ID=flight_num)
        except models_app.Flight.DoesNotExist:
            return Response(status=404)
        serializer = FlightSerializer(flight)

        return Response(serializer.data)


# TODO: попробовать переписать на generic
# TODO: написать вью для бронирования и покупки
class BuyTicket(APIView):
    """Бронирование билетов"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TicketBuySerializer(data=request.data)
        if serializer.is_valid():

            try:
                ticket = models_app.Ticket.objects.get(pk=serializer.validated_data.get('id'))
            except models_app.Ticket.DoesNotExist:
                return Response(serializer.errors, status=404)

            # TODO: Проверка документа(в зав от возраста) и подсчет сколько лет на момент ВЫЛЕТА, скидка детям
            passenger, _ = models_app.Passenger.objects.get_or_create(**serializer.validated_data.get("passenger"))
            ticket.passenger = passenger
            ticket.customer = self.request.user
            ticket.save()
            return Response(status=204)
        else:
            return Response(serializer.errors, status=404)




