from django.shortcuts import render, redirect, get_object_or_404
from .models import Filiere, EmploiDuTemps
from django.contrib import messages
from django.views.decorators.http import require_POST
from accounts.models import Utilisateur # Importation de votre modèle Utilisateur personnalisé
from django.db import models
from django.contrib.auth.decorators import login_required  # Django gère cela nativement et de façon très puissante grâce au décorateur @login_required


# ==========================================
# VUE : LISTE DES FORMATIONS
# ==========================================
def formations_view(request):
    """
    Récupère toutes les filières enregistrées en base de données 
    et les envoie au template pour affichage.
    """
    # Extraction de la totalité des enregistrements de la table Filiere
    filieres = Filiere.objects.all()
    
    # Rendu de la page avec injection des données récupérées
    return render(request, 'formation.html', {'filieres': filieres})


# ==========================================
# VUE : CONSULTATION DE L'EMPLOI DU TEMPS
# ==========================================
def emploi_du_temps_public(request):
    """
    Vue publique affichant la grille de cours filtrée par filière et par niveau.
    Gère la récupération dynamique des cours selon les choix de l'utilisateur.
    """
    # Récupération de toutes les filières pour alimenter le menu déroulant du formulaire de filtrage
    filieres = Filiere.objects.all()
    
    # Captation des critères de recherche envoyés via l'URL (?filiere_id=X&niveau_etude=Y)
    filiere_id = request.GET.get('filiere_id')
    niveau_selectionne = request.GET.get('niveau_etude')
    
    # Initialisation des variables qui contiendront les résultats de la recherche
    emplois = None
    filiere_selectionnee = None
    periode_semaine = "Période non définie"
    
    # Liste brute des niveaux d'études pour générer manuellement les options dans le template
    CHOICES_NIVEAU = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2']
    
    # Déclenchement de la recherche uniquement si l'utilisateur a sélectionné une filière ET un niveau
    if filiere_id and niveau_selectionne:
        # Recherche sécurisée de la filière demandée (renvoie None si l'ID n'existe pas)
        filiere_selectionnee = Filiere.objects.filter(pk=filiere_id).first()
        
        # Si la filière existe bien en base de données
        if filiere_selectionnee:
            # Filtrage des cours correspondants à la fois à la filière et au niveau d'étude
            # Les cours sont triés selon l'ordre défini par défaut (jour, heure_debut)
            emplois = EmploiDuTemps.objects.filter(
                filiere=filiere_selectionnee,
                niveau_etude=niveau_selectionne
            ).order_by('jour', 'heure_debut')
            
            # Extraction dynamique de la semaine de cours
            # On prend la valeur du champ 'semaine_du' stockée dans le tout premier cours trouvé
            premier_cours = emplois.first()
            if premier_cours:
                periode_semaine = premier_cours.semaine_du

    # Construction du dictionnaire de contexte destiné à alimenter le code HTML du template
    context = {
        'filieres': filieres,                         # Liste de toutes les filières (pour le formulaire)
        'choices_niveau': CHOICES_NIVEAU,             # Liste des niveaux (pour le formulaire)
        'emplois': emplois,                           # Liste des cours trouvés (ou None si aucune recherche)
        'filiere_selectionnee': filiere_selectionnee, # Objet filière actuellement filtré
        'niveau_selectionne': niveau_selectionne,     # Chaîne du niveau actuellement filtré
        'periode_semaine': periode_semaine,           # Texte de la période de la semaine à afficher en titre
    }
    
    # Rendu final du template HTML de l'emploi du temps public avec ses données
    return render(request, 'academics/timetable_public.html', context)


from django.shortcuts import render
from .models import Filiere, EmploiDuTemps

# ==========================================
# VUE : INTERFACE DE GESTION DU PLANNING (ADMIN)
# ==========================================
def gestion_planning_admin(request):
    """
    Interface graphique de gestion sur mesure pour l'administrateur.
    Organise les cours de manière flexible sous forme de listes quotidiennes.
    """
    # Récupération de toutes les filières pour le formulaire de sélection initial
    filieres = Filiere.objects.all()
    
    # Captation des filtres de sélection de la classe (Filière + Niveau) passés en GET
    filiere_id = request.GET.get('filiere_id')
    niveau_selectionne = request.GET.get('niveau_etude')
    
    # Initialisation des variables de contrôle et de stockage
    emplois = None
    filiere_selectionnee = None
    periode_semaine = "Semaine en cours"
    
    # Listes de référence pour la génération des choix et l'ordre des jours
    CHOICES_NIVEAU = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2']
    JOURS = ['LUNDI', 'MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI']

    # ÉTAPE 1 : Extraction des cours en base de données selon le filtre appliqué
    if filiere_id and niveau_selectionne:
        filiere_selectionnee = Filiere.objects.filter(pk=filiere_id).first()
        if filiere_selectionnee:
            # Récupération des cours de la classe, classés chronologiquement par heure de début
            emplois = EmploiDuTemps.objects.filter(
                filiere=filiere_selectionnee,
                niveau_etude=niveau_selectionne
            ).order_by('jour', 'heure_debut')
            
            # Mise à jour du libellé de la semaine basé sur le premier cours enregistré
            premier = emplois.first()
            if premier:
                periode_semaine = premier.semaine_du

    # ÉTAPE 2 : Initialisation d'un dictionnaire indexé par jour (Clé: JOUR, Valeur: [Liste des cours])
    grille_jours = {jour: [] for jour in JOURS}
    
    # ÉTAPE 3 : Distribution et répartition libre de chaque cours dans son jour respectif
    if emplois:
        for c in emplois:
            # Sécurité pour vérifier que le jour du cours est bien présent dans notre liste de référence
            if c.jour in grille_jours:
                grille_jours[c.jour].append(c)

    # ÉTAPE 4 : Restructuration des données sous forme de liste de dictionnaires pour faciliter la boucle du template
    grille_html = []
    for jour in JOURS:
        grille_html.append({
            'nom_jour': jour,                 # Nom du jour (ex: LUNDI)
            'cours_liste': grille_jours[jour] # Tous les objets EmploiDuTemps rattachés à ce jour
        })

    # ÉTAPE 5 : Préparation et envoi du contexte global au template de gestion
    context = {
        'filieres': filieres,
        'choices_niveau': CHOICES_NIVEAU,
        'filiere_selectionnee': filiere_selectionnee,
        'niveau_selectionne': niveau_selectionne,
        'periode_semaine': periode_semaine,
        'grille_html': grille_html, # Structure finale imbriquée contenant le planning trié
    }
    
    # Rendu de la page d'administration visuelle
    return render(request, 'academics/gestion_planning.html', context)




# ==========================================
# VUE : AJOUT OU MODIFICATION RAPIDE DE COURS
# ==========================================
@require_POST  # Sécurité : Restreint l'accès à cette vue aux seules requêtes de type POST
def ajouter_cours_rapide(request):
    """
    Contrôleur gérant dynamiquement la création et la modification d'un cours en base de données.
    Redirige l'utilisateur vers le planning filtré après traitement.
    """
    try:
        # Récupération sécurisée de la filière (renvoie une erreur 404 si l'identifiant n'existe pas)
        filiere = get_object_or_404(Filiere, pk=request.POST.get('filiere_id'))
        niveau = request.POST.get('niveau_etude')
        cours_id = request.POST.get('cours_id')  # Récupère l'ID (présent uniquement en cas de modification)
        
        # Dictionnaire associant les champs du modèle aux données soumises par le formulaire
        data_champs = {
            'filiere': filiere,
            'niveau_etude': niveau,
            'semaine_du': request.POST.get('semaine_du', 'Semaine en cours'),
            'nom_matiere': request.POST.get('nom_matiere'),
            'enseignant': request.POST.get('enseignant'),
            'jour': request.POST.get('jour'),
            'heure_debut': request.POST.get('heure_debut'),
            'heure_fin': request.POST.get('heure_fin'),
            'salle': request.POST.get('salle')
        }

        # Vérification de la présence d'un identifiant de cours valide pour basculer entre UPDATE et INSERT
        if cours_id and str(cours_id).strip() and str(cours_id) != 'None':
            # CAS 1 : L'ID existe -> Modification du cours existant via l'opérateur d'inférence (**)
            EmploiDuTemps.objects.filter(pk=cours_id).update(**data_champs)
            messages.success(request, "Planification mise à jour avec succès !")
        else:
            # CAS 2 : Pas d'ID -> Création d'une nouvelle entrée en base de données
            EmploiDuTemps.objects.create(**data_champs)
            messages.success(request, "Nouvelle planification enregistrée avec succès !")

    except Exception as e:
        # Capture de toute anomalie de saisie ou de base de données et stockage du message d'erreur
        messages.error(request, f"Erreur de traitement : {e}")
        
    # Redirection automatique vers le tableau de bord de gestion avec maintien des filtres actifs
    return redirect(f"/academics/gestion-planning/?filiere_id={filiere.pk}&niveau_etude={niveau}")


# ==========================================
# VUE : SUPPRESSION RAPIDE D'UN COURS
# ==========================================
@require_POST  # Sécurité : Empêche la suppression accidentelle via une simple URL GET
def supprimer_cours_rapide(request, pk):
    """
    Supprime un cours en un seul clic depuis la grille d'administration.
    Mémorise le contexte de la classe pour rediriger l'utilisateur sur le même écran.
    """
    # Récupération de l'objet à supprimer ou génération d'une page 404
    cours = get_object_or_404(EmploiDuTemps, pk=pk)
    
    # Sauvegarde des paramètres de la classe avant destruction de l'objet
    filiere_id = cours.filiere.pk
    niveau = cours.niveau_etude
    
    # Retrait définitif de l'enregistrement en base de données
    cours.delete()
    
    # Notification positive envoyée au système de messages Django
    messages.success(request, "Cours retiré du planning.")
    
    # Redirection propre vers la grille de gestion de la classe concernée
    return redirect(f"/academics/gestion-planning/?filiere_id={filiere_id}&niveau_etude={niveau}")


# ==========================================
# VUE : ANNUAIRE PUBLIC DES ALUMNI
# ==========================================
@login_required  # <-- Force la connexion avant de voir les profils
def annuaire_alumni_public(request):
    """
    Affiche l'annuaire des anciens diplômés de l'IBAM.
    Permet une recherche croisée par filière d'origine et par mots-clés textuels.
    """
    # Récupération de toutes les filières pour alimenter les critères de sélection du formulaire
    filieres = Filiere.objects.all()
    
    # Lecture des filtres de recherche saisis par le visiteur (?filiere_id=X&q=texte)
    filiere_id = request.GET.get('filiere_id')
    recherche_nom = request.GET.get('q')
    
    # ÉTAPE 1 : Extraction initiale de tous les utilisateurs possédant un rôle rattaché aux anciens élèves
    diplomes = Utilisateur.objects.filter(role_user__in=['ALUMNI', 'Anciens élèves', 'Anciens elèves'])
    
    # ÉTAPE 2 : Application du filtre par filière d'étude (si une valeur non vide est soumise)
    if filiere_id and filiere_id.strip():
        diplomes = diplomes.filter(filiere_id=filiere_id)
        
    # ÉTAPE 3 : Application de la recherche textuelle insensible à la casse (icontains)
    if recherche_nom and recherche_nom.strip():
        mot_cle = recherche_nom.strip()
        # Requête complexe utilisant Q() pour chercher le mot-clé dans le prénom, le nom OU le pseudo
        diplomes = diplomes.filter(
            models.Q(first_name__icontains=mot_cle) | 
            models.Q(last_name__icontains=mot_cle) | 
            models.Q(username__icontains=mot_cle)
        )
        
    # Préparation de l'ensemble des données pour l'injection dans le template HTML
    context = {
        'filieres': filieres,                       # Liste des filières pour le menu déroulant
        'diplomes': diplomes,                       # Liste filtrée des anciens élèves à afficher
        'filiere_selectionnee_id': filiere_id,       # ID mémorisé pour laisser la filière sélectionnée active
        'recherche_nom': recherche_nom,             # Texte mémorisé pour le réafficher dans la barre de recherche
    }
    
    # Rendu graphique de la page de l'annuaire
    return render(request, 'alumni/alumni.html', context)