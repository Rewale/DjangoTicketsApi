from typing import Optional, Any

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Field
from django.forms import ModelForm

from django.http import HttpRequest
from django.urls import resolve
from django.utils.safestring import mark_safe

from . import models


#  https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Admin_site
# TODO: Подставлять возраст на МОМЕНТ вылета
class TicketsInstanceInline(admin.TabularInline):
    """Билеты"""
    model = models.Ticket
    extra = 1

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        seq_value_default = 1
        if db_field.name == 'Seq':
            try:
                resolved = resolve(request.path_info)
                print(resolved)
                if resolved.kwargs:
                    print(resolved.kwargs)
                    seq_value_default = self.parent_model.objects.get(
                        pk=resolved.kwargs['object_id']).tickets.last().Seq + 1

            except:
                print("АШиПКА!!!")
                # seq_value_default = 1
            kwargs['initial'] = seq_value_default
            print(seq_value_default)

        return super().formfield_for_dbfield(db_field, request, **kwargs)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(kwargs)
        # if db_field.name == "Customer":
        # kwargs["initial"] = request.
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('Flight_ID', 'DateFrom', 'DateTo', 'airTo', 'airFrom')
    # fields = ['Flight_ID', ('DateFrom', 'DateTo'), ('airTo', 'airFrom')]

    fieldsets = (
        (None, {
            'fields': ('Flight_ID', 'Company')
        }),
        ('Время', {
            'fields': ('DateFrom', 'DateTo')
        }),
        ('Место вылета/Прилета', {
            'fields': ['airTo', 'airFrom']
        })
    )

    inlines = [TicketsInstanceInline]


@admin.register(models.Passenger)
class PassengerAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["document"].help_text = "Паспорт - для взрослых, свидетельство о рождении - для лиц младше 14"
        return form

    def clean_document(self):
        document = self.cleaned_data['document']
        get_age = self.cleaned_data['get_age']

        if get_age() < 14:
            raise ValidationError('Свидетельство о рождении')
        else:
            raise ValidationError('Паспорт')

        return document


admin.site.register(models.AirCompany)
admin.site.register(models.Airport)
admin.site.register(models.Town)
admin.site.register(models.Country)

