# Generated by Django 3.2.8 on 2021-11-26 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_rename_miles_authuser_miles'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='accept_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
