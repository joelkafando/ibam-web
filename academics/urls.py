from django.urls import path
from . import views  # Importation des vues du dossier courant pour les lier aux URL

# Espace de noms de l'application (permet d'utiliser 'academics:nom_route' dans les templates et redirections)
app_name = 'academics'

urlpatterns = [
    # Route pour la consultation de l'emploi du temps par les étudiants et le grand public
    path('programme/', views.emploi_du_temps_public, name='timetable_public'),
    
    # ==========================================
    # ROUTES DE GESTION VISUELLE (ESPACE ADMIN)
    # ==========================================
    
    # Page principale du tableau de bord de gestion du planning
    path('gestion-planning/', views.gestion_planning_admin, name='gestion_planning_admin'),
    
    # Route pour traiter l'ajout rapide d'un cours depuis l'interface visuelle
    path('gestion-planning/ajouter/', views.ajouter_cours_rapide, name='ajouter_cours_rapide'),
    
    # Route pour supprimer un cours spécifique via son identifiant unique (clé primaire 'pk')
    path('gestion-planning/supprimer/<int:pk>/', views.supprimer_cours_rapide, name='supprimer_cours_rapide'),
    
    # ==========================================
    # AUTRES SERVICES
    # ==========================================
    
    # Route pour consulter l'annuaire public des anciens étudiants (Alumni)
    path('alumni/', views.annuaire_alumni_public, name='annuaire_alumni_public'),
]
