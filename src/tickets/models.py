from datetime import datetime, date, time, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accessify import private

from src.oauth.models import AuthUser
from src.tickets.services.TicketCustomerWOEscort import TicketCustomerWOEscort


class AirCompany(models.Model):
    """Авиакомпания - поставщик билетов"""
    icon = models.ImageField()
    name = models.CharField(max_length=50)
    discount_for_INF = models.IntegerField("Скидка для детей младше 2 лет", default=90)
    discount_for_CHD = models.IntegerField("Скидка для детей от 2 до 14 лет", default=50)

    class Meta:
        verbose_name = 'Авиакомпания'
        verbose_name_plural = 'Авиакомпании'

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    """Страна"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return f'{self.name}'


class Town(models.Model):
    """Город"""
    name = models.CharField(max_length=100)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name="country")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name}, {self.country}'


class Airport(models.Model):
    """Аэропорт"""
    IATA_code = models.CharField(max_length=3, primary_key=True)
    town = models.ForeignKey(to=Town, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'

    def __str__(self):
        return f'{self.IATA_code}({self.town})'


class Flight(models.Model):
    """Рейс"""
    flight_ID = models.CharField(max_length=6, primary_key=True, verbose_name="Номер рейса")
    dateFrom = models.DateTimeField(verbose_name="Время вылета")
    dateTo = models.DateTimeField(verbose_name="Время прилета (прибл.)")
    # Gate = models.DateTimeField()
    # CountOfTickets = models.IntegerField()
    airFrom = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name="airFrom", verbose_name="Вылет из"
                                , default=None)
    airTo = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name='airTo', verbose_name="Прилет в"
                              , default=None)
    company = models.ForeignKey(to=AirCompany, on_delete=models.CASCADE, related_name='company',
                                verbose_name="Компания")
    miles = models.FloatField(verbose_name="Количетсво миль", default=0)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    def __str__(self):
        return f'{self.flight_ID}'


class Passenger(models.Model):
    """Пассажир"""
    # passportSeries = models.CharField(max_length=4, primary_key=True, verbose_name="Серия паспорта")
    # passportNum = models.CharField(max_length=6, verbose_name="Номер паспорта")
    document = models.CharField(verbose_name="Документ", max_length=25, primary_key=True)
    birthDate = models.DateField(verbose_name="День рождения")
    citizenship = models.ForeignKey(verbose_name="Гражданство", to=Country, related_name="citizens", on_delete=models.CASCADE)
    FIO = models.CharField("ФИО", max_length=100)

    def get_age(self, start_date=datetime.today().date()):
        end_date = self.birthDate
        difference = start_date - end_date
        difference_in_years = round((difference.days + difference.seconds / 86400) / 365.2425)
        print(difference_in_years)
        return difference_in_years

    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'

    def __str__(self):
        return f'{self.FIO}:{self.get_age()}'


class Ticket(models.Model):
    # TODO: Проблема с добавлением айди вместо Seq (на крайняк создавать БД заново)
    """Билет"""

    class Meta:
        unique_together = (('seat', 'flightOfTicket'),)
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    flightOfTicket = models.ForeignKey(to=Flight, on_delete=models.CASCADE, related_name='tickets')

    cost = models.IntegerField(verbose_name="Цена")
    seat = models.CharField(max_length=5, verbose_name="Место")

    passenger = models.ForeignKey(to=Passenger, on_delete=models.CASCADE, verbose_name="Пассажир",
                                  default=None, null=True, blank=True, related_name='seat')

    escort_passenger = models.ForeignKey(to=Passenger, on_delete=models.CASCADE, verbose_name="Пассажир",
                                         default=None, null=True, blank=True, related_name='escort')

    customer = models.ForeignKey(to=AuthUser, on_delete=models.CASCADE, verbose_name="Покупатель", default=None,
                                 null=True, blank=True)

    is_bought = models.BooleanField(verbose_name="Куплен?", default=False)

    @property
    def seat_passenger(self):
        return self.passenger

    @property
    def escort_passenger_prop(self):
        return self.escort_passenger

    @escort_passenger_prop.setter
    def escort_passenger_prop(self, value):
        if value.get_age() < 16:
            raise TicketEscortException
        self.escort_passenger = value

    @seat_passenger.setter  # property-name.setter decorator
    def seat_passenger(self, value: Passenger):
        if value.get_age() < 16 and self.escort_passenger is None:
            raise TicketCustomerWOEscort
        self.passenger = value

    @property
    def price_prop(self):
        if 16 > self.passenger.get_age() > 2:
            return self.cost - (self.cost * self.flightOfTicket.company.discount_for_CHD/100)
        elif self.passenger.get_age() < 2:
            return self.cost - (self.cost * self.flightOfTicket.company.discount_for_INF/100)
        else:
            return self.cost

    def __str__(self):
        return f'{self.flightOfTicket}:{self.seat}'
