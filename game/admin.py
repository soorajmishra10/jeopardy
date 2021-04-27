from django.contrib import admin
from game.models import Room, RoomLobby, Leaderboard, Question
# Register your models here.

admin.site.register(Room)
admin.site.register(RoomLobby)
admin.site.register(Leaderboard)
admin.site.register(Question)
