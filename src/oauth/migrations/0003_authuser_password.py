# Generated by Django 3.2.8 on 2021-11-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0002_auto_20211121_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='password',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]