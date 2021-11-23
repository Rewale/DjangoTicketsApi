from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import get_path_upload_avatar, validate_size_image


class AuthUser(models.Model):
    """
    Модель пользователя на платформе
    """
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    miles = models.FloatField(default=0)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        # unique_together = (('passportSeries', 'passportNum'),)
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    @property
    def is_authenticated(self):
        """Всегда возвращает True. Способ узнать, был ли пользователь аутентифицирован"""
        return True

    def __str__(self):
        return self.email

