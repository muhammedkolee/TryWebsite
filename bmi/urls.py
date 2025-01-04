from django.urls import path
from . import views

urlpatterns = [
    path('', views.bmi, name='bmi'),
    path('result', views.result, name='result')
]