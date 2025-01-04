from django.urls import path
from . import views

urlpatterns = [
    path('', views.apis, name='apis'),
    path('soccer', views.soccer, name='soccer'),
    path('matches', views.matches, name='matches'),
    path('weather', views.weather, name='weather'),
    path('currency', views.currency, name='currency'),
]