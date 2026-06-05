from django.urls import path
from .views import IBAMLoginView, register_student, modifier_mon_profil  # Importation des vues d'authentification et de profil
from django.contrib.auth.views import LogoutView

# Espace de noms de l'application pour isoler et appeler ces routes via 'accounts:nom_route'
app_name = 'accounts'

urlpatterns = [
    # Route pour la page de connexion (utilise une vue basée sur une classe réécrite sur mesure)
    path('login/', IBAMLoginView.as_view(), name='login'),
    
    # Route pour la déconnexion (utilise la vue de déconnexion native et sécurisée de Django)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Route pour accéder au formulaire d'inscription des nouveaux étudiants (Admissions)
    path('admissions/', register_student, name='register'),
    
    # ==========================================
    # ESPACE PORTAIL ÉTUDIANT (NOUVEAU)
    # ==========================================
    
    # Route permettant à l'étudiant connecté de modifier lui-même ses données personnelles
    path('portail/etudiant/modifier/', modifier_mon_profil, name='modifier_profil'),
]
