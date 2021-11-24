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
from .serializers import TicketSerializer, FlightSerializer, NumFlightSerializer


class UsersTickets(generics.ListAPIView):
    """Список билетов купленных пользователем"""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer_serialized = UserSerializer(self.request.user)
        # print(customer_serialized.data)

        tickets = models_app.Ticket.objects.filter(Customer__id=customer_serialized.data['id'])

        return tickets


class TicketsListView(generics.ListAPIView):
    """Вывод списка билетов"""
    serializer_class = TicketSerializer

    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = service.MovieFilter
    # permission_classes = [permissions.IsAuthenticated]

    # Не выводим купленные билеты
    def get_queryset(self):
        tickets = models_app.Ticket.objects.filter(Customer=None)

        return tickets


# TODO: нормально передавать параметры в запросе
class TicketsInFlightListView(APIView):
    """Вывод билетов определенного рейса"""

    def post(self, request):
        user_data = NumFlightSerializer(data=request.data)
        if user_data.is_valid():
            flight_num = user_data.data['FlightNum']
            print(flight_num)
            if flight_num:
                tickets = models_app.Ticket.objects.filter(FlightOfTicket=flight_num, Customer=None)
            else:
                tickets = models_app.Ticket.objects.filter(Customer=None)
            serializer = TicketSerializer(tickets, many=True)

            return Response(serializer.data)


class FlightListView(generics.ListAPIView):
    serializer_class = FlightSerializer

    def get_queryset(self):
        flights = models_app.Flight.objects.annotate(count_tickets=models.Count('tickets'))

        return flights


@api_view(('POST',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def buy_ticket(request, flight_num, seq):

    ticket = models_app.Ticket.objects.get(FlightOfTicket=flight_num, Seq=seq)

    if ticket.Customer is not None:
        return Response(data='{"Response"=Neok, "detail"="Билет уже куплен"}', status=403)

    ticket.Customer = models_app.Customer.objects.first()
    ticket.save()

    return Response(data='{"Response"="ok", "detail"="Билет приобритен"}', status=200)


