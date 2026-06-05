from django.urls import path
from . import views

app_name = 'alumni'

urlpatterns = [
    path('', views.liste_alumni, name='reseau_alumni'),
]
