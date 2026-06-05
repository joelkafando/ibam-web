from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academics.models import EmploiDuTemps  # Extraction du modèle pour l'alimentation de l'intranet

# ==========================================
# 1. TABLEAU DE BORD : ADMINISTRATION
# ==========================================
@login_required  # Sécurité : Restreint l'accès aux seuls utilisateurs authentifiés
def admin_dashboard(request):
    """
    Espace d'accueil et de pilotage réservé à la direction 
    et aux administrateurs de la plateforme.
    """
    return render(request, 'dashboard/admin_dashboard.html')


# ==========================================
# 2. TABLEAU DE BORD : ENSEIGNANT
# ==========================================
@login_required  # Sécurité : Restreint l'accès aux seuls utilisateurs authentifiés
def teacher_dashboard(request):
    """
    Espace de suivi pédagogique réservé exclusivement 
    au corps enseignant pour la gestion de leurs interventions.
    """
    return render(request, 'dashboard/teacher_dashboard.html')


# ==========================================
# 3. TABLEAU DE BORD : ÉTUDIANT
# ==========================================
@login_required  # Sécurité : Restreint l'accès aux seuls utilisateurs authentifiés
def student_dashboard(request):
    """
    Espace d'accueil de l'intranet réservé aux étudiants de l'IBAM.
    Affiche un aperçu personnalisé basé sur leur profil.
    """
    user = request.user
    context = {}
    
    # ÉTAPE 1 : Récupération automatique des cours liés à la filière de l'étudiant connecté (Filtre RBAC strict)
    if hasattr(user, 'filiere') and user.filiere:
        # Filtrage de tous les cours rattachés à sa filière d'origine, classés par jour et heure de début
        context['emplois'] = EmploiDuTemps.objects.filter(filiere=user.filiere).order_by('jour', 'heure_debut')
        
        # Extraction du tout premier cours trié chronologiquement pour alimenter un widget d'alerte sur l'interface
        context['prochain_cours'] = context['emplois'].first()
    else:
        # Mesure de sécurité si le compte étudiant n'est rattaché à aucune filière en base de données
        context['emplois'] = None
        context['prochain_cours'] = None

    # Rendu graphique du tableau de bord de l'étudiant avec ses données contextuelles
    return render(request, 'dashboard/student_dashboard.html', context)


# ==========================================
# 4. VUE PUBLIC : ADMISSIONS
# ==========================================
def admissions_view(request):
    """
    Affiche la page d'information publique concernant les conditions d'admission, 
    les grilles de tarifs et les procédures administratives de l'IBAM.
    """
    return render(request, 'core/admissions.html')


# ==========================================
# 5. VUE : EMPLOI DU TEMPS ÉTUDIANT (DÉSACTIVÉE / EN ATTENTE)
# ==========================================
# @login_required
# def student_timetable(request):
#     """
#     Page dédiée à l'affichage de l'emploi du temps complet et détaillé de l'étudiant connecté.
#     Cette section est actuellement mise en commentaire pour une activation future.
#     """
#     user = request.user
#     context = {}
#     
#     # Vérification de l'existence de la filière sur le compte de l'utilisateur
#     if hasattr(user, 'filiere') and user.filiere:
#         # Extraction de l'ensemble des cours de la formation
#         emplois = EmploiDuTemps.objects.filter(filiere=user.filiere).order_by('jour', 'heure_debut')
#         context['emplois'] = emplois
#         
#         # Récupération des informations de période et de niveau basées sur le premier enregistrement trouvé
#         premier_cours = emplois.first()
#         if premier_cours:
#             context['periode_semaine'] = premier_cours.semaine_du
#             context['mention_niveau'] = premier_cours.niveau_etude
#         else:
#             # Valeurs par défaut si la grille horaire de la filière est actuellement vide
#             context['periode_semaine'] = "Semaine non définie"
#             context['mention_niveau'] = "Niveau non défini"
#     else:
#         # Valeurs de repli si l'utilisateur connecté ne possède pas de profil étudiant valide
#         context['emplois'] = None
#         context['periode_semaine'] = "Période non définie"
#         context['mention_niveau'] = "Filière non définie"
#
#     # Rendu du template dédié au calendrier individuel de l'étudiant
#     return render(request, 'dashboard/student_timetable.html', context)
