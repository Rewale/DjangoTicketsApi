# Generated by Django 3.2.8 on 2021-11-23 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passenger',
            options={'verbose_name': 'Пассажир', 'verbose_name_plural': 'Пассажиры'},
        ),
    ]
