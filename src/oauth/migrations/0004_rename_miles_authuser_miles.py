# Generated by Django 3.2.8 on 2021-11-23 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_authuser_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authuser',
            old_name='Miles',
            new_name='miles',
        ),
    ]