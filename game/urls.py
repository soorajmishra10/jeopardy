from django.urls import path
from game import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/login/', views.login_view, name='login_view'),
    path('game/signup/', views.register_view, name='register_view'),
    path('game/home/', views.home_view, name='home_view'),
    path('game/play/<room_code>/', views.play_view, name='play_view'),
    path('game/logout_view', views.logout_view, name='logout_view'),
]
