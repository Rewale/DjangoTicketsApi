from rest_framework import serializers
from . import models


class TicketSerializer(serializers.ModelSerializer):
    """Список билетов"""

    class Meta:
        model = models.Ticket
        fields = ('FlightOfTicket', 'Seq', 'Cost', 'Seat')


# TODO: серилизовать компанию
class CompanySerializer(serializers.ModelSerializer):
    """Серилизатор компании"""
    class Meta:
        model = models.AirCompany
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    """Список рейсов"""
    count_tickets = serializers.IntegerField()
    Company = CompanySerializer()

    class Meta:
        model = models.Flight
        fields = ('Flight_ID', 'DateFrom', 'DateTo', 'airFrom', 'airTo', 'Company', 'count_tickets')


