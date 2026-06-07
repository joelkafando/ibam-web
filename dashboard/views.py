# Importation des fonctions utilitaires de Django pour le rendu et la redirection
from django.shortcuts import render, redirect

# Importation du décorateur qui protège les vues aux utilisateurs connectés uniquement
from django.contrib.auth.decorators import login_required

# Importation du système de messages flash de Django (succès, erreurs, alertes)
from django.contrib import messages

# Importation des modèles de données nécessaires depuis l'application "academics"
from academics.models import EmploiDuTemps, RessourcePedagogique, DisponibiliteEnseignant, Filiere

# Importation du décorateur personnalisé qui restreint l'accès aux enseignants et admins uniquement
from .decorators import enseignant_requis

# Importation des formulaires créés dans le fichier forms.py du même module
from .forms import DepotCoursForm, DisponibiliteForm


# ==========================================
# 1. TABLEAU DE BORD : ADMINISTRATION
# ==========================================

# Protection de la vue : seul un utilisateur connecté peut y accéder
@login_required
def admin_dashboard(request):
    """
    Espace d'accueil et de pilotage réservé à la direction.
    Affiche les rapports de disponibilité envoyés par les profs
    pour aider à concevoir le planning.
    """

    # Construction du contexte de données à transmettre au template HTML
    context = {
        # Récupération de toutes les disponibilités des enseignants,
        # triées de la plus récente à la plus ancienne (signe "-" = ordre décroissant)
        'disponibilites_profs': DisponibiliteEnseignant.objects.all().order_by('-date_soumission')
    }

    # Rendu du template HTML avec les données du contexte
    return render(request, 'dashboard/admin_dashboard.html', context)


# ==========================================
# 2. TABLEAU DE BORD : ENSEIGNANT (LOGIQUE COMPLÈTE)
# ==========================================

# Décorateur personnalisé : bloque l'accès si l'utilisateur n'est pas enseignant ou admin
@enseignant_requis
def teacher_dashboard(request):
    """
    Espace de suivi pédagogique complet réservé au corps enseignant de l'IBAM.
    Gère le calendrier, le téléversement de fichiers et les demandes de créneaux.
    """

    # Récupération de l'objet utilisateur actuellement connecté
    user = request.user

    # Initialisation du dictionnaire de contexte qui sera passé au template
    context = {}

    # =========================================================================
    # ÉTAPE A : Récupération des données liées à l'enseignant connecté
    # =========================================================================

    # Filtrage des cours de l'emploi du temps appartenant à cet enseignant,
    # triés par jour puis par heure de début pour un affichage chronologique
    context['mes_cours'] = EmploiDuTemps.objects.filter(enseignant=user).order_by('jour', 'heure_debut')

    # Récupération de tous les fichiers de cours déposés par cet enseignant
    context['mes_depots'] = RessourcePedagogique.objects.filter(enseignant=user)

    # Récupération de toutes les disponibilités soumises par cet enseignant
    context['mes_dispos_soumises'] = DisponibiliteEnseignant.objects.filter(enseignant=user)

    # =========================================================================
    # ÉTAPE B : Pré-chargement des formulaires vides pour l'affichage initial
    # =========================================================================

    # Formulaire vide pour le dépôt d'un nouveau support de cours
    context['form_cours'] = DepotCoursForm()

    # Formulaire vide pour la soumission d'une disponibilité horaire
    context['form_dispo'] = DisponibiliteForm()

    # =========================================================================
    # ÉTAPE C : Traitement des soumissions (requêtes HTTP de type POST uniquement)
    # =========================================================================
    if request.method == 'POST':

        # Cas 1 : L'enseignant a cliqué sur le bouton de dépôt de cours
        if 'btn_depot_cours' in request.POST:

            # Instanciation du formulaire avec les données POST et les fichiers uploadés
            form_cours = DepotCoursForm(request.POST, request.FILES)

            # Vérification de la validité des données saisies
            if form_cours.is_valid():

                # Création de l'objet en mémoire sans le sauvegarder encore en base (commit=False)
                # Cela permet d'injecter manuellement l'enseignant avant la sauvegarde définitive
                cours = form_cours.save(commit=False)

                # Injection de l'enseignant connecté comme auteur du dépôt
                cours.enseignant = user

                # Sauvegarde définitive de l'objet en base de données
                cours.save()

                # Affichage d'un message de succès dynamique avec le titre du cours
                messages.success(request, f"Le document '{cours.titre_cours}' a été mis en ligne avec succès pour les étudiants !")

                # Redirection vers le tableau de bord pour éviter la re-soumission du formulaire (pattern PRG)
                return redirect('dashboard:teacher_dashboard')

            else:
                # En cas d'erreur, on réinjecte le formulaire avec ses erreurs dans le contexte
                # pour que l'utilisateur puisse les corriger
                context['form_cours'] = form_cours

        # Cas 2 : L'enseignant a cliqué sur le bouton de soumission de disponibilité
        elif 'btn_soumission_dispo' in request.POST:

            # Instanciation du formulaire avec les données POST (pas de fichier ici)
            form_dispo = DisponibiliteForm(request.POST)

            # Vérification de la validité des données saisies
            if form_dispo.is_valid():

                # Création de l'objet en mémoire sans sauvegarde immédiate
                dispo = form_dispo.save(commit=False)

                # Injection de l'enseignant connecté comme propriétaire de la disponibilité
                dispo.enseignant = user

                # Sauvegarde définitive en base de données
                dispo.save()

                # Message de confirmation affiché à l'enseignant après soumission
                messages.success(request, "Vos préférences horaires ont bien été transmises au Directeur des Études !")

                # Redirection pour éviter la re-soumission accidentelle (pattern PRG)
                return redirect('dashboard:teacher_dashboard')

            else:
                # En cas d'erreur de validation, on réinjecte le formulaire avec ses erreurs
                context['form_dispo'] = form_dispo

    # Rendu final du template avec toutes les données du contexte
    return render(request, 'dashboard/teacher_dashboard.html', context)


# ==========================================
# 3. TABLEAU DE BORD : ÉTUDIANT (LOGIQUE DE L'INTRANET RESSOURCES)
# ==========================================

# Protection de la vue : l'étudiant doit être connecté pour y accéder
@login_required
def student_dashboard(request):
    """
    Espace d'accueil de l'intranet réservé aux étudiants de l'IBAM.
    Affiche l'emploi du temps ET les documents de cours déposés
    par les profs pour la classe de l'étudiant connecté.
    """

    # Récupération de l'objet utilisateur connecté
    user = request.user

    # Initialisation du dictionnaire de contexte
    context = {}

    # Vérification que l'étudiant possède bien une filière associée à son profil
    if hasattr(user, 'filiere') and user.filiere:

        # Filtrage de l'emploi du temps selon la filière ET le niveau d'études de l'étudiant
        # Tri chronologique : d'abord par jour, ensuite par heure de début
        context['emplois'] = EmploiDuTemps.objects.filter(
            filiere=user.filiere,
            niveau_etude=user.niveau_etude
        ).order_by('jour', 'heure_debut')

        # Extraction du prochain cours à venir (premier résultat du queryset trié)
        context['prochain_cours'] = context['emplois'].first()

        # Récupération sécurisée du niveau d'études de l'étudiant
        # Si l'attribut n'existe pas, on utilise "Licence 1" comme valeur par défaut
        niveau_eleve = getattr(user, 'niveau_etude', 'Licence 1')

        # Filtrage des ressources pédagogiques disponibles UNIQUEMENT pour
        # la filière et le niveau d'études de l'étudiant connecté
        context['mes_ressources_cours'] = RessourcePedagogique.objects.filter(
            filiere=user.filiere,
            niveau_etude=user.niveau_etude
        )

    else:
        # Si l'étudiant n'a pas de filière renseignée, on passe des valeurs nulles
        # pour éviter les erreurs dans le template HTML
        context['emplois'] = None
        context['prochain_cours'] = None
        context['mes_ressources_cours'] = None

    # Rendu du template étudiant avec toutes les données filtrées
    return render(request, 'dashboard/student_dashboard.html', context)


# ==========================================
# 4. VUE PUBLIQUE : ADMISSIONS
# ==========================================

def admissions_view(request):
    """
    Affiche la page d'information publique concernant les conditions d'admission,
    les grilles de tarifs et les procédures administratives de l'IBAM.
    Aucune authentification requise : accessible à tous les visiteurs.
    """

    # Rendu simple du template statique des admissions, sans données dynamiques
    return render(request, 'core/admissions.html')