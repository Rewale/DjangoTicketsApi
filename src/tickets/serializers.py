from rest_framework import serializers
from . import models

# TODO:Получение рейса со всеми некупленными билетами (listserializer),
# TODO:Пересмотреть гайды по выводу списков и серилизаторам, привязка свойства?
# TODO:Покупка билетов, urls:create,


class CompanySerializer(serializers.ModelSerializer):
    """Серилизатор компании"""
    class Meta:
        model = models.AirCompany
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """Список билетов"""

    class Meta:
        model = models.Ticket
        fields = ('Seq', 'Cost', 'Seat')


class FlightSerializer(serializers.ModelSerializer):
    """Список рейсов"""
    # count_tickets = serializers.IntegerField()
    Company = CompanySerializer()
    tickets = TicketSerializer()

    class Meta:
        model = models.Flight
        fields = ('Flight_ID', 'DateFrom', 'DateTo', 'airFrom', 'airTo', 'Company', 'tickets')


class NumFlightSerializer(serializers.Serializer):
    FlightNum = serializers.CharField()











