# Importation de la fonction 'path' de Django pour définir les routes URL
from django.urls import path

# Importation du module views du dossier courant (même application)
# Donne accès à toutes les fonctions/classes de vues définies dans views.py
from . import views


# Espace de noms de l'application : permet d'éviter les conflits de noms entre applications
# Utilisation dans les templates : {% url 'academics:timetable_public' %}
# Utilisation dans le code Python : reverse('academics:timetable_public')
app_name = 'academics'


# Liste des correspondances URL → Vue de l'application 'academics'
# Django parcourt cette liste de haut en bas jusqu'à trouver une correspondance
urlpatterns = [

    # -----------------------------------------------------------------------
    # Route publique : accessible par les étudiants et visiteurs sans connexion
    # URL complète (selon inclusion dans urls.py principal) : /academics/programme/
    # Vue appelée : views.emploi_du_temps_public
    # Nom de la route : 'academics:timetable_public' (utilisable dans les templates)
    # -----------------------------------------------------------------------
    path('programme/', views.emploi_du_temps_public, name='timetable_public'),


    # ==========================================
    # ROUTES DE GESTION VISUELLE (ESPACE ADMIN)
    # ==========================================

    # -----------------------------------------------------------------------
    # Tableau de bord principal de gestion du planning (réservé aux admins)
    # URL complète : /academics/gestion-planning/
    # Vue appelée : views.gestion_planning_admin
    # Nom de la route : 'academics:gestion_planning_admin'
    # -----------------------------------------------------------------------
    path('gestion-planning/', views.gestion_planning_admin, name='gestion_planning_admin'),

    # -----------------------------------------------------------------------
    # Route pour traiter le formulaire d'ajout rapide d'un cours
    # URL complète : /academics/gestion-planning/ajouter/
    # Vue appelée : views.ajouter_cours_rapide (gère en général une requête POST)
    # Nom de la route : 'academics:ajouter_cours_rapide'
    # -----------------------------------------------------------------------
    path('gestion-planning/ajouter/', views.ajouter_cours_rapide, name='ajouter_cours_rapide'),

    # -----------------------------------------------------------------------
    # Route pour supprimer un cours identifié par sa clé primaire (pk)
    # URL complète : /academics/gestion-planning/supprimer/12/ (ex: pk=12)
    # <int:pk> : paramètre dynamique entier capturé depuis l'URL et transmis à la vue
    # Vue appelée : views.supprimer_cours_rapide(request, pk=12)
    # Nom de la route : 'academics:supprimer_cours_rapide'
    # -----------------------------------------------------------------------
    path('gestion-planning/supprimer/<int:pk>/', views.supprimer_cours_rapide, name='supprimer_cours_rapide'),


    # ==========================================
    # AUTRES SERVICES
    # ==========================================

    # -----------------------------------------------------------------------
    # Route pour l'annuaire public des anciens étudiants (Alumni)
    # URL complète : /academics/alumni/
    # Vue appelée : views.annuaire_alumni_public
    # Nom de la route : 'academics:annuaire_alumni_public'
    # -----------------------------------------------------------------------
    path('alumni/', views.annuaire_alumni_public, name='annuaire_alumni_public'),
]