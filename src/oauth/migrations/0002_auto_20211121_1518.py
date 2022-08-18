# Generated by Django 3.2.8 on 2021-11-21 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallink',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='authuser',
            options={'verbose_name': 'Покупатель', 'verbose_name_plural': 'Покупатели'},
        ),
        migrations.RemoveField(
            model_name='authuser',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='authuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='authuser',
            name='display_name',
        ),
        migrations.AddField(
            model_name='authuser',
            name='Miles',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
        migrations.DeleteModel(
            name='SocialLink',
        ),
    ]