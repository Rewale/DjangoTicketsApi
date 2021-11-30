from datetime import datetime, date, time, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from src.oauth.models import AuthUser


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
    Flight_ID = models.CharField(max_length=6, primary_key=True, verbose_name="Номер рейса")
    DateFrom = models.DateTimeField(verbose_name="Время вылета")
    DateTo = models.DateTimeField(verbose_name="Время прилета (прибл.)")
    # Gate = models.DateTimeField()
    # CountOfTickets = models.IntegerField()
    airFrom = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name="airFrom", verbose_name="Вылет из"
                                , default=None)
    airTo = models.ForeignKey(to=Airport, on_delete=models.CASCADE, related_name='airTo', verbose_name="Прилет в"
                              , default=None)
    Company = models.ForeignKey(to=AirCompany, on_delete=models.CASCADE, related_name='company',
                                verbose_name="Компания")
    Miles = models.FloatField(verbose_name="Количетсво миль", default=0)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'

    def __str__(self):
        return f'{self.Flight_ID}'


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
        unique_together = (('Seat', 'FlightOfTicket'),)
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    FlightOfTicket = models.ForeignKey(to=Flight, on_delete=models.CASCADE, related_name='tickets')

    Seq = models.IntegerField(primary_key=True, verbose_name="Номер",
                              default=1)

    Cost = models.IntegerField(verbose_name="Цена")
    Seat = models.CharField(max_length=5, verbose_name="Место")

    Passenger = models.ForeignKey(to=Passenger, on_delete=models.CASCADE, verbose_name="Пассажир",
                                  default=None, null=True, blank=True)
    Customer = models.ForeignKey(to=AuthUser, on_delete=models.CASCADE, verbose_name="Покупатель", default=None,
                                 null=True, blank=True)

    Is_bought = models.BooleanField(verbose_name="Куплен?", default=False)

    def __str__(self):
        return f'{self.FlightOfTicket}:{self.Seat}'
