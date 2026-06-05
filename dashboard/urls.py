from django.urls import path
from . import views

# Espace de noms de l'application (permet d'utiliser 'dashboard:nom_route' dans vos redirections d'authentification)
app_name = 'dashboard'

urlpatterns = [
    # Route d'accès à l'espace de pilotage et d'administration générale de l'établissement
    path('portail/administration/', views.admin_dashboard, name='admin_dashboard'),
    
    # Route d'accès à l'espace de suivi pédagogique réservé aux professeurs et intervenants
    path('portail/enseignant/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Route d'accès au profil d'accueil et au suivi de scolarité de l'étudiant connecté
    path('portail/etudiant/', views.student_dashboard, name='student_dashboard'),
    
    # ==========================================
    # OPTIONS INDIVIDUELLES ÉTUDIANTES (EN ATTENTE)
    # ==========================================
    # Route future en attente d'activation pour afficher le calendrier des cours propre à l'élève connecté
    # path('portail/etudiant/emploi-du-temps/', views.student_timetable, name='student_timetable'),
]
