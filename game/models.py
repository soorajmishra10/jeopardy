from django.db import models

# Create your models here.
class Room(models.Model):
    room_code = models.CharField(max_length=256, unique=True)
    room_host = models.EmailField()
    room_size = models.IntegerField()
    game_started = models.BooleanField(default=False)
    turn = models.IntegerField(default=-1)
    is_round_over = models.BooleanField(default=True)

    def __str__(self):
        return self.room_code

class RoomLobby(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_code = models.CharField(max_length=256)
    room_user = models.CharField(max_length=256)
    score = models.IntegerField(default=0)
    is_online = models.BooleanField(default=False)
    user_id = models.IntegerField()

    def __str__(self):
        return self.room_code


class Leaderboard(models.Model):
    username = models.EmailField(unique=True)
    highscore = models.IntegerField()

    def __str__(self):
        return self.username


class Question(models.Model):
    question_no = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=256)
    points = models.IntegerField()

    def __str__(self):
        return self.question
    
