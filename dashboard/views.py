from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from academics.models import EmploiDuTemps, RessourcePedagogique, DisponibiliteEnseignant, Filiere
from .decorators import enseignant_requis  # On importe le verrou de sécurité strict pour les profs
from .forms import DepotCoursForm, DisponibiliteForm

# ==========================================
# 1. TABLEAU DE BORD : ADMINISTRATION
# ==========================================
@login_required
def admin_dashboard(request):
    """
    Espace d'accueil et de pilotage réservé à la direction.
    Ajout des rapports de dispo envoyés par les profs pour concevoir le planning.
    """
    context = {
        'disponibilites_profs': DisponibiliteEnseignant.objects.all().order_by('-date_soumission')
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ==========================================
# 2. TABLEAU DE BORD : ENSEIGNANT (LOGIQUE COMPLÈTE)
# ==========================================
@enseignant_requis  # Sécurité stricte : Seuls les enseignants ou admins accèdent ici
def teacher_dashboard(request):
    """
    Espace de suivi pédagogique complet réservé au corps enseignant de l'IBAM.
    Gère son calendrier, le téléversement de fichiers et ses demandes de créneaux.
    """
    user = request.user
    context = {}
    
    # =========================================================================
    # CORRECTION ICI : Liaison relationnelle directe via l'ID de l'enseignant connecté
    # =========================================================================
    context['mes_cours'] = EmploiDuTemps.objects.filter(enseignant=user).order_by('jour', 'heure_debut')
    
    # ÉTAPE B : Récupération de l'historique de ses propres cours déposés et de ses disponibilités
    context['mes_depots'] = RessourcePedagogique.objects.filter(enseignant=user)
    context['mes_dispos_soumises'] = DisponibiliteEnseignant.objects.filter(enseignant=user)

    # ÉTAPE C : Initialisation des deux formulaires d'action
    context['form_cours'] = DepotCoursForm()
    context['form_dispo'] = DisponibiliteForm()

    # ÉTAPE D : Traitement des soumissions de formulaires (POST)
    if request.method == 'POST':
        if 'btn_depot_cours' in request.POST:
            form_cours = DepotCoursForm(request.POST, request.FILES)
            if form_cours.is_valid():
                cours = form_cours.save(commit=False)
                cours.enseignant = user  
                cours.save()
                messages.success(request, f"Le document '{cours.titre_cours}' a été mis en ligne avec succès pour les étudiants !")
                return redirect('dashboard:teacher_dashboard')
            else:
                context['form_cours'] = form_cours 
                
        elif 'btn_soumission_dispo' in request.POST:
            form_dispo = DisponibiliteForm(request.POST)
            if form_dispo.is_valid():
                dispo = form_dispo.save(commit=False)
                dispo.enseignant = user
                dispo.save()
                messages.success(request, "Vos préférences horaires ont bien été transmises au Directeur des Études !")
                return redirect('dashboard:teacher_dashboard')
            else:
                context['form_dispo'] = form_dispo

    return render(request, 'dashboard/teacher_dashboard.html', context)



# ==========================================
# 3. TABLEAU DE BORD : ÉTUDIANT (LOGIQUE DE L'INTRANET RESSOURCES)
# ==========================================
@login_required
def student_dashboard(request):
    """
    Espace d'accueil de l'intranet réservé aux étudiants de l'IBAM.
    Affiche l'emploi du temps ET les documents de cours déposés par les profs pour sa classe.
    """
    user = request.user
    context = {}
    
    if hasattr(user, 'filiere') and user.filiere:
        # Filtrage croisé exact : Emploi du temps lié à sa filière et sa classe
        context['emplois'] = EmploiDuTemps.objects.filter(
            filiere=user.filiere,
            niveau_etude=user.niveau_etude
        ).order_by('jour', 'heure_debut')
        
        context['prochain_cours'] = context['emplois'].first()
        # Filtre 2 (NOUVEAU) : Extraction des fichiers de cours partagés par les enseignants pour SA classe !
        # On croise sa filière d'origine ET son niveau d'études (si le champ niveau_etude existe sur votre modèle Utilisateur)
        niveau_eleve = getattr(user, 'niveau_etude', 'Licence 1')
        # Le filtrage des cours devient imperméable grâce au nouveau champ physique de l'utilisateur
        context['mes_ressources_cours'] = RessourcePedagogique.objects.filter(
            filiere=user.filiere,
            niveau_etude=user.niveau_etude
        )
    else:
        context['emplois'] = None
        context['prochain_cours'] = None
        context['mes_ressources_cours'] = None

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
