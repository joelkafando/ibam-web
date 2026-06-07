# Importation des fonctions utilitaires de Django pour le rendu, les redirections et la gestion des 404
from django.shortcuts import render, redirect, get_object_or_404

# Importation des modèles Filiere et EmploiDuTemps de l'application courante
from .models import Filiere, EmploiDuTemps

# Importation du système de messages flash Django (alertes succès, erreur, info affichées à l'utilisateur)
from django.contrib import messages

# Importation du décorateur qui restreint une vue aux seules requêtes HTTP POST
from django.views.decorators.http import require_POST

# Importation du modèle Utilisateur personnalisé depuis l'application 'accounts'
from accounts.models import Utilisateur

# Importation du module models pour utiliser les objets Q() dans les requêtes complexes
from django.db import models

# Importation du décorateur qui force la connexion avant d'accéder à une vue protégée
from django.contrib.auth.decorators import login_required

# Importation de la fonction qui retourne dynamiquement le modèle User actif du projet
# (préférable à un import direct car respecte le paramètre AUTH_USER_MODEL dans settings.py)
from django.contrib.auth import get_user_model


# ==========================================
# VUE : LISTE DES FORMATIONS
# ==========================================

# Fonction vue classique Django (Function-Based View) accessible sans authentification
def formations_view(request):
    """
    Récupère toutes les filières enregistrées en base de données
    et les envoie au template pour affichage.
    """
    # Extraction de la totalité des enregistrements de la table Filiere
    # .all() génère un QuerySet contenant tous les objets Filiere sans filtre
    filieres = Filiere.objects.all()

    # Rendu du template HTML 'formation.html' avec injection du QuerySet des filières
    # Le dictionnaire {'filieres': filieres} rend la variable accessible dans le template
    return render(request, 'formation.html', {'filieres': filieres})


# ==========================================
# VUE : CONSULTATION DE L'EMPLOI DU TEMPS
# ==========================================

# Vue publique : aucune restriction d'accès, visible par tous les visiteurs
def emploi_du_temps_public(request):
    """
    Vue publique affichant la grille de cours filtrée par filière et par niveau.
    Gère la récupération dynamique des cours selon les choix de l'utilisateur.
    """
    # Récupération de toutes les filières pour alimenter le menu déroulant du formulaire de filtrage
    filieres = Filiere.objects.all()

    # Lecture du paramètre 'filiere_id' passé dans l'URL via GET (ex: ?filiere_id=3)
    # .get() retourne None si le paramètre est absent, sans lever d'exception
    filiere_id = request.GET.get('filiere_id')

    # Lecture du paramètre 'niveau_etude' passé dans l'URL via GET (ex: &niveau_etude=Licence+1)
    niveau_selectionne = request.GET.get('niveau_etude')

    # Initialisation à None : aucun cours affiché tant que l'utilisateur n'a pas filtré
    emplois = None

    # Initialisation à None : aucune filière sélectionnée par défaut
    filiere_selectionnee = None

    # Valeur par défaut du libellé de la semaine affiché dans le titre de la grille
    periode_semaine = "Période non définie"

    # Liste statique des niveaux d'études disponibles pour générer les options du formulaire HTML
    CHOICES_NIVEAU = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2']

    # Déclenchement de la recherche uniquement si les deux critères sont fournis simultanément
    if filiere_id and niveau_selectionne:

        # Recherche sécurisée de la filière par clé primaire
        # .filter().first() retourne None si aucun résultat (contrairement à .get() qui lèverait une exception)
        filiere_selectionnee = Filiere.objects.filter(pk=filiere_id).first()

        # Vérification que la filière existe bien en base de données avant d'aller plus loin
        if filiere_selectionnee:

            # Filtrage des cours correspondant exactement à la filière ET au niveau sélectionnés
            # .order_by('jour', 'heure_debut') : tri chronologique par jour puis par heure de début
            emplois = EmploiDuTemps.objects.filter(
                filiere=filiere_selectionnee,       # Filtre sur l'objet Filiere (clé étrangère)
                niveau_etude=niveau_selectionne     # Filtre sur le niveau d'étude (chaîne de caractères)
            ).order_by('jour', 'heure_debut')       # Tri : d'abord par jour, puis par heure

            # Extraction du libellé de la semaine depuis le premier cours du résultat
            # .first() retourne None si le QuerySet est vide (aucun cours planifié)
            premier_cours = emplois.first()
            if premier_cours:
                # Récupération de la valeur du champ 'semaine_du' du premier cours trouvé
                periode_semaine = premier_cours.semaine_du

    # Dictionnaire de contexte : toutes les données transmises au template pour l'affichage
    context = {
        'filieres': filieres,                           # QuerySet de toutes les filières (menu déroulant)
        'choices_niveau': CHOICES_NIVEAU,               # Liste des niveaux d'études (menu déroulant)
        'emplois': emplois,                             # QuerySet des cours filtrés (None si pas de filtre)
        'filiere_selectionnee': filiere_selectionnee,   # Objet Filiere actif (pour pré-sélectionner le formulaire)
        'niveau_selectionne': niveau_selectionne,       # Chaîne du niveau actif (pour pré-sélectionner le formulaire)
        'periode_semaine': periode_semaine,             # Libellé de la semaine affiché dans le titre de la grille
    }

    # Rendu du template de l'emploi du temps public avec toutes les données du contexte
    return render(request, 'academics/timetable_public.html', context)


# ==========================================
# VUE : INTERFACE DE GESTION DU PLANNING (ADMIN)
# ==========================================

# Importations redondantes placées ici dans le code source original (déjà importées en haut du fichier)
from django.shortcuts import render
from .models import Filiere, EmploiDuTemps

# Vue réservée à l'administration : gestion visuelle complète des emplois du temps
def gestion_planning_admin(request):
    """
    Interface graphique de gestion sur mesure pour l'administrateur.
    Organise les cours sous forme de listes quotidiennes et traite la planification en POST.
    """
    # Récupération de toutes les filières pour le formulaire de sélection de la classe
    filieres = Filiere.objects.all()

    # Lecture des paramètres de filtrage passés via l'URL (méthode GET)
    filiere_id = request.GET.get('filiere_id')
    niveau_selectionne = request.GET.get('niveau_etude')

    # Initialisation des variables avant toute logique conditionnelle
    emplois = None
    filiere_selectionnee = None
    periode_semaine = "Semaine en cours"    # Libellé de semaine par défaut si aucun cours n'est trouvé

    # Listes de référence statiques utilisées pour les menus et l'ordre d'affichage des jours
    CHOICES_NIVEAU = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2']
    JOURS = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI']  # Ordre d'affichage des colonnes

    # Récupération dynamique du modèle User actif (respecte AUTH_USER_MODEL dans settings.py)
    # Filtre les utilisateurs ayant exactement le rôle 'ENSEIGNANT' (insensible à la casse grâce à iexact)
    Utilisateur = get_user_model()
    tous_les_profs = Utilisateur.objects.filter(role_user__iexact='ENSEIGNANT').order_by('username')

    # ÉTAPE 1 : Extraction des cours si les deux critères de filtre sont présents dans l'URL
    if filiere_id and niveau_selectionne:

        # Recherche sécurisée de la filière (retourne None si inexistante, pas d'exception)
        filiere_selectionnee = Filiere.objects.filter(pk=filiere_id).first()

        if filiere_selectionnee:

            # Traitement du formulaire d'ajout de cours soumis en méthode POST
            if request.method == 'POST':

                # Extraction de chaque champ du formulaire depuis les données POST
                nom_matiere = request.POST.get('nom_matiere')       # Nom de la matière saisie
                enseignant_id = request.POST.get('enseignant')      # ID numérique de l'enseignant sélectionné
                jour = request.POST.get('jour')                     # Jour de la semaine choisi
                heure_debut = request.POST.get('heure_debut')       # Heure de début du cours
                heure_fin = request.POST.get('heure_fin')           # Heure de fin du cours
                salle = request.POST.get('salle')                   # Salle où se déroulera le cours
                # Semaine concernée (valeur par défaut si champ vide)
                semaine_du = request.POST.get('semaine_du', 'Semaine en cours')

                try:
                    # Récupération de l'instance réelle de l'enseignant depuis sa clé primaire
                    # Indispensable car Django exige un objet, pas un simple ID textuel pour les ForeignKey
                    prof_instance = Utilisateur.objects.get(id=enseignant_id)

                    # Création et enregistrement immédiat du cours en base de données
                    # Chaque paramètre correspond à un champ du modèle EmploiDuTemps
                    EmploiDuTemps.objects.create(
                        filiere=filiere_selectionnee,       # Objet Filiere (clé étrangère)
                        niveau_etude=niveau_selectionne,    # Niveau d'étude sélectionné (ex: 'Licence 2')
                        nom_matiere=nom_matiere,            # Nom de la matière à planifier
                        enseignant=prof_instance,           # Instance Utilisateur (pas l'ID brut !)
                        jour=jour,                          # Jour de la semaine (ex: 'LUNDI')
                        heure_debut=heure_debut,            # Heure de début (format HH:MM)
                        heure_fin=heure_fin,                # Heure de fin (format HH:MM)
                        salle=salle,                        # Identifiant de la salle (ex: 'Salle A12')
                        semaine_du=semaine_du               # Libellé de la semaine concernée
                    )
                    # Affichage d'un message de confirmation vert dans l'interface
                    messages.success(request, "La séance de cours a été planifiée avec succès dans la grille graphique !")

                    # Redirection vers la même page avec les mêmes filtres pour actualiser la grille
                    return redirect(f'/academics/gestion-planning/?filiere_id={filiere_id}&niveau_etude={niveau_selectionne}')

                except Utilisateur.DoesNotExist:
                    # Cas où l'ID enseignant soumis ne correspond à aucun utilisateur en base de données
                    messages.error(request, "Erreur : L'enseignant sélectionné est introuvable.")

                except Exception as e:
                    # Capture générique de toutes les autres erreurs imprévues avec affichage du détail
                    messages.error(request, f"Erreur de traitement : {str(e)}")

            # Récupération des cours de la classe filtrée, triés chronologiquement
            emplois = EmploiDuTemps.objects.filter(
                filiere=filiere_selectionnee,
                niveau_etude=niveau_selectionne
            ).order_by('jour', 'heure_debut')   # Tri : par jour puis par heure de début

            # Mise à jour du libellé de la semaine à partir du premier cours enregistré
            premier = emplois.first()   # Récupère le premier cours du QuerySet (ou None si vide)
            if premier:
                periode_semaine = premier.semaine_du    # Lecture du champ 'semaine_du' du premier cours

    # ÉTAPE 2 : Création d'un dictionnaire avec un jour comme clé et une liste vide comme valeur initiale
    # Exemple résultat : {'LUNDI': [], 'MARDI': [], 'MERCREDI': [], ...}
    grille_jours = {jour: [] for jour in JOURS}

    # ÉTAPE 3 : Répartition de chaque cours dans la liste correspondant à son jour
    if emplois:
        for c in emplois:
            # Vérification défensive : le jour du cours doit exister dans le dictionnaire
            if c.jour in grille_jours:
                # Ajout de l'objet cours dans la liste du jour correspondant
                grille_jours[c.jour].append(c)

    # ÉTAPE 4 : Conversion du dictionnaire en liste ordonnée de dictionnaires pour la boucle du template
    # Format final : [{'nom_jour': 'LUNDI', 'cours_liste': [...]}, {'nom_jour': 'MARDI', ...}, ...]
    grille_html = []
    for jour in JOURS:
        grille_html.append({
            'nom_jour': jour,                   # Clé 'nom_jour' : utilisée dans le template pour afficher le titre du jour
            'cours_liste': grille_jours[jour]   # Clé 'cours_liste' : liste des cours à afficher sous ce jour
        })

    # ÉTAPE 5 : Assemblage du contexte complet et envoi au template de gestion visuelle
    context = {
        'filieres': filieres,                           # Toutes les filières (menu déroulant de filtrage)
        'choices_niveau': CHOICES_NIVEAU,               # Tous les niveaux (menu déroulant de filtrage)
        'filiere_selectionnee': filiere_selectionnee,   # Objet Filiere actif (pour pré-sélectionner le menu)
        'niveau_selectionne': niveau_selectionne,       # Niveau actif (pour pré-sélectionner le menu)
        'periode_semaine': periode_semaine,             # Libellé de la semaine affiché dans le titre de la grille
        'grille_html': grille_html,                     # Structure de données pour afficher la grille par jour
        'tous_les_profs': tous_les_profs,               # QuerySet des enseignants pour le menu déroulant du formulaire
    }

    # Rendu du template de l'interface de gestion du planning avec toutes les données préparées
    return render(request, 'academics/gestion_planning.html', context)


# ==========================================
# VUE : AJOUT RAPIDE DE COURS
# ==========================================

# Décorateur de sécurité : bloque toute tentative d'accès à cette URL via une requête GET
# Seules les soumissions de formulaire (POST) sont autorisées à déclencher cette vue
@require_POST
def ajouter_cours_rapide(request):
    """
    Contrôleur gérant la création d'une séance de cours en base de données de façon relationnelle.
    Redirige l'administrateur vers le planning filtré après traitement.
    """
    # Récupération du modèle User actif défini dans settings.AUTH_USER_MODEL
    Utilisateur = get_user_model()

    # Initialisation des variables de contexte utilisées pour la redirection finale
    filiere = None  # Sera rempli si la filière est trouvée
    niveau = None   # Sera rempli si le niveau est fourni dans le formulaire

    try:
        # Récupération sécurisée de la filière cible via sa clé primaire
        # get_object_or_404 : retourne automatiquement une page 404 si l'ID est invalide ou absent
        filiere = get_object_or_404(Filiere, pk=request.POST.get('filiere_id'))

        # Lecture du niveau d'étude soumis dans le formulaire
        niveau = request.POST.get('niveau_etude')

        # Lecture de l'ID numérique de l'enseignant sélectionné dans le menu déroulant (ex: "8")
        enseignant_id = request.POST.get('enseignant')

        # Récupération de l'instance complète de l'utilisateur enseignant depuis son ID
        # get_object_or_404 : retourne une 404 si l'ID ne correspond à aucun utilisateur
        prof_instance = get_object_or_404(Utilisateur, id=enseignant_id)

        # Création et enregistrement immédiat du cours en base de données
        EmploiDuTemps.objects.create(
            filiere=filiere,                                        # Objet Filiere (relation ForeignKey)
            niveau_etude=niveau,                                    # Niveau d'études cible
            semaine_du=request.POST.get('semaine_du', 'Semaine en cours'),  # Semaine (valeur par défaut si absent)
            nom_matiere=request.POST.get('nom_matiere'),            # Nom de la matière enseignée
            enseignant=prof_instance,                               # Objet Utilisateur enseignant (pas l'ID brut !)
            jour=request.POST.get('jour').upper(),                  # Jour forcé en majuscules (ex: 'lundi' → 'LUNDI')
            heure_debut=request.POST.get('heure_debut'),            # Heure de début du cours (format HH:MM)
            heure_fin=request.POST.get('heure_fin'),                # Heure de fin du cours (format HH:MM)
            salle=request.POST.get('salle')                         # Salle ou amphi du cours
        )

        # Affichage d'un message flash de confirmation visible sur la page suivante
        messages.success(request, "Nouvelle planification enregistrée avec succès !")

    except Exception as e:
        # Capture de toute erreur inattendue et affichage d'un message d'erreur rouge à l'utilisateur
        messages.error(request, f"Erreur de traitement : {e}")

    # Redirection vers la grille filtrée si les deux paramètres sont disponibles
    if filiere and niveau:
        # Retour vers la page de gestion avec les mêmes filtres de classe actifs
        return redirect(f"/academics/gestion-planning/?filiere_id={filiere.pk}&niveau_etude={niveau}")

    # Redirection de secours vers la page de gestion sans filtre si un paramètre est manquant
    return redirect("/academics/gestion-planning/")


# ==========================================
# VUE : SUPPRESSION RAPIDE D'UN COURS
# ==========================================

# Décorateur de sécurité : empêche la suppression accidentelle par simple navigation via URL (GET)
# La suppression ne peut être déclenchée que par une soumission de formulaire POST
@require_POST
def supprimer_cours_rapide(request, pk):
    """
    Supprime définitivement un cours en un clic depuis la grille d'administration.
    Mémorise le contexte de la classe pour ré-afficher le même écran filtré.
    """
    # Récupération sécurisée du cours ciblé par sa clé primaire (pk transmis dans l'URL)
    # Retourne automatiquement une page 404 si le cours est introuvable ou déjà supprimé
    cours = get_object_or_404(EmploiDuTemps, pk=pk)

    # Sauvegarde de la clé primaire de la filière AVANT suppression
    # (après .delete(), l'objet n'est plus accessible et ses attributs seraient perdus)
    filiere_id = cours.filiere.pk

    # Sauvegarde du niveau d'étude AVANT suppression pour restaurer le filtre après redirection
    niveau = cours.niveau_etude

    # Suppression définitive de l'enregistrement dans la base de données
    # Génère une requête SQL : DELETE FROM academics_emploidutemps WHERE id = pk
    cours.delete()

    # Message flash de confirmation affiché sur la page suivante après redirection
    messages.success(request, "La séance de cours a été retirée du planning avec succès.")

    # Redirection vers la grille de gestion en conservant les mêmes filtres de classe
    # L'utilisateur retrouve exactement le même écran filtré qu'avant la suppression
    return redirect(f"/academics/gestion-planning/?filiere_id={filiere_id}&niveau_etude={niveau}")


# ==========================================
# VUE : ANNUAIRE PUBLIC DES ALUMNI
# ==========================================

# Décorateur qui exige une session authentifiée avant d'accéder à cette vue
# Si non connecté, Django redirige automatiquement vers la page de login (LOGIN_URL dans settings.py)
@login_required
def annuaire_alumni_public(request):
    """
    Affiche l'annuaire des anciens diplômés.
    Permet une recherche croisée par filière d'origine et par mots-clés textuels.
    """
    # Récupération de toutes les filières pour alimenter le menu déroulant du formulaire de filtrage
    filieres = Filiere.objects.all()

    # Lecture du filtre par filière passé dans l'URL (ex: ?filiere_id=2)
    filiere_id = request.GET.get('filiere_id')

    # Lecture du mot-clé de recherche textuelle passé dans l'URL (ex: &q=dupont)
    recherche_nom = request.GET.get('q')

    # ÉTAPE 1 : Extraction de base de tous les utilisateurs ayant un rôle Alumni
    # role_user__in : filtre sur une liste de valeurs possibles (équivalent SQL : WHERE role_user IN (...)
    diplomes = Utilisateur.objects.filter(role_user__in=['ALUMNI', 'Anciens élèves', 'Anciens elèves'])

    # ÉTAPE 2 : Affinage optionnel du QuerySet par filière si le paramètre est présent et non vide
    if filiere_id and filiere_id.strip():   # .strip() : élimine les espaces parasites autour de la valeur
        # Filtre supplémentaire sur la filière liée à l'utilisateur Alumni
        diplomes = diplomes.filter(filiere_id=filiere_id)

    # ÉTAPE 3 : Affinage optionnel par mot-clé textuel si la barre de recherche a été utilisée
    if recherche_nom and recherche_nom.strip():
        mot_cle = recherche_nom.strip()     # Nettoyage des espaces inutiles avant/après la saisie

        # Requête OR complexe avec Q() : cherche le mot-clé dans le prénom, le nom OU le pseudo
        # | est l'opérateur logique OR entre deux objets Q()
        # icontains : recherche insensible à la casse (ex: "dupont" trouvera "Dupont" et "DUPONT")
        diplomes = diplomes.filter(
            models.Q(first_name__icontains=mot_cle) |  # Recherche dans le prénom
            models.Q(last_name__icontains=mot_cle) |   # OU dans le nom de famille
            models.Q(username__icontains=mot_cle)      # OU dans le nom d'utilisateur
        )

    # Préparation du dictionnaire de contexte pour le template de l'annuaire
    context = {
        'filieres': filieres,                           # Toutes les filières (menu déroulant)
        'diplomes': diplomes,                           # QuerySet filtré des alumni à afficher
        'filiere_selectionnee_id': filiere_id,          # ID mémorisé pour pré-sélectionner la filière dans le formulaire
        'recherche_nom': recherche_nom,                 # Texte mémorisé pour le réafficher dans la barre de recherche
    }

    # Rendu du template de l'annuaire avec toutes les données de contexte injectées
    return render(request, 'alumni/alumni.html', context)