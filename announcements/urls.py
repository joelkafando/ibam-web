from django.urls import path
from . import views  # Importation des vues du module courant pour les associer aux chemins d'URL

# Espace de noms de l'application permettant d'isoler ces routes (ex: {% url 'announcements:announcements' %})
app_name = 'announcements'

urlpatterns = [
    # Route principale : Affiche la liste complète de toutes les annonces actives
    path('', views.announcement_list, name='announcements'),
    
    # ==========================================
    # LECTURE COMPLÈTE (DÉTAIL D'UNE ANNONCE)
    # ==========================================
    
    # Route dynamique : Récupère l'identifiant unique (clé primaire 'pk') sous forme d'entier
    # Permet de charger et de lire une annonce spécifique en intégralité
    path('<int:pk>/', views.announcement_detail, name='announcement_detail'),
]
