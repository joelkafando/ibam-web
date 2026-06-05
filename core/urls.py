from django.urls import path
from . import views  # Importation des vues du module core pour les associer aux chemins d'URL

urlpatterns = [
    # Route de la page d'accueil principale du site web
    path('', views.home, name='home'),
    
    # Route vers la page présentant l'offre de formation globale de l'établissement
    path('formations/', views.formations, name='formations'),
    
    # Route vers la page d'explication des procédures d'admission et d'inscription
    path('admissions/', views.admissions, name='admissions'),
    
    # Route vers le formulaire de contact (Note : Pensez à renommer la fonction en contact_view dans views.py)
    path('contact/', views.contact, name='contact'),

    # ==========================================
    # ROUTES DYNAMIQUES DU MENU "L'IBAM"
    # ==========================================
    
    # Route vers la page de présentation générale et des missions (charge le template about.html)
    path('about/', views.about, name='presentation'),
    
    # Route vers la page retraçant l'historique de l'établissement
    path('ibam/historique/', views.historique, name='historique'),
    
    # Route vers la page présentant les membres de l'équipe dirigeante et administrative
    path('ibam/equipe-dirigeante/', views.equipe, name='equipe'),
]
