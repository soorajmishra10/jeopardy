# Generated by Django 3.2 on 2021-04-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_roomlobby_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='turn',
            field=models.IntegerField(default=-1),
        ),
    ]
