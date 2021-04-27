# Generated by Django 3.2 on 2021-04-17 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=254, unique=True)),
                ('highscore', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=256, unique=True)),
                ('room_host', models.EmailField(max_length=254)),
                ('room_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomLobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=256)),
                ('room_user', models.CharField(max_length=256)),
                ('score', models.IntegerField(default=0)),
                ('is_online', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.room')),
            ],
        ),
    ]
