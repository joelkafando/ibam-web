from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index_forum, name='index'),
    path('nouveau/', views.creer_sujet, name='creer_sujet'),
    path('discussion/<int:pk>/', views.detail_sujet, name='detail_sujet'),
    path('categorie/<int:pk>/', views.sujets_par_categorie, name='sujets_par_categorie'),
]
