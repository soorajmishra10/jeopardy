from django.urls import path

from game import consumers

websocket_urlpatterns = [
    path('ws/game/play/<room_code>', consumers.GameConsumer.as_asgi()),
]