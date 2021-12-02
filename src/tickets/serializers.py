from rest_framework import serializers
from . import models
from collections import OrderedDict
# TODO:Получение рейса со всеми некупленными билетами (listserializer),
# TODO:Пересмотреть гайды по выводу списков и серилизаторам, привязка свойства?
# TODO:Покупка билетов, urls:create,


class CompanySerializer(serializers.ModelSerializer):
    """Серилизатор компании"""
    class Meta:
        model = models.AirCompany
        fields = '__all__'


class TicketDetailSerializer(serializers.ModelSerializer):
    """Полная информация о билете"""
    class Meta:
        model = models.Ticket
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    """Билет в списке"""

    class Meta:
        model = models.Ticket
        fields = ('cost', 'seat', 'flightOfTicket')

    # TODO: другой способ скрыть купленные билеты - сделать антацию рейса со списком не купленных билетов
    def to_representation(self, instance: models.Ticket):
        if instance.customer is not None:
            return
        return super().to_representation(instance=instance)


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Passenger
        fields = '__all__'
        # Отключаем валидацию на уникальность
        extra_kwargs = {
            "document": {
                "validators": [],
            },
        }


class TicketBuySerializer(serializers.Serializer):
    """Покупка билета"""
    id = serializers.IntegerField()
    passenger = PassengerSerializer()


class FlightSerializer(serializers.ModelSerializer):
    """Информация о рейсе со всеми билетами"""
    count_tickets = serializers.IntegerField()
    company = CompanySerializer()
    tickets = TicketSerializer(many=True)

    class Meta:
        model = models.Flight
        fields = ('flight_ID', 'dateFrom', 'dateTo', 'airFrom', 'airTo', 'company', 'count_tickets', 'tickets')


