# Importation de la fonction render pour générer une réponse HTTP à partir d'un template HTML
# et d'un dictionnaire de contexte contenant les données à afficher
from django.shortcuts import render

# Importation de Q : objet Django permettant de construire des requêtes complexes
# avec des opérateurs logiques OR (|) et AND (&) dans les filtres de QuerySet
from django.db.models import Q

# Importation du modèle Filiere depuis l'application academics
# Permet d'alimenter le menu déroulant de filtrage par formation
from academics.models import Filiere

# Importation du modèle User personnalisé depuis l'application accounts
# Contient tous les comptes utilisateurs dont les Alumni filtrables par rôle
from accounts.models import User

# Importation du décorateur de protection des vues par authentification
# Redirige automatiquement vers la page de login si l'utilisateur n'est pas connecté
from django.contrib.auth.decorators import login_required


# ==========================================
# VUE : LISTE ET FILTRAGE DES ALUMNI
# ==========================================

# Décorateur appliqué à la vue : bloque tout accès anonyme à cette page
# Un visiteur non connecté sera redirigé vers LOGIN_URL défini dans settings.py
@login_required
def liste_alumni(request):
    """
    Vue filtrant et affichant le réseau des anciens étudiants (Alumni)
    conformément au module 2.2.5 du cahier des charges.
    """

    # ÉTAPE 1 : Extraction initiale de tous les utilisateurs ayant le rôle 'alumni'
    # .filter(role='alumni') : génère un SELECT SQL WHERE role = 'alumni'
    # Retourne un QuerySet (liste d'objets) non encore évalué (lazy evaluation)
    # ⚠️ Ajustez 'role="alumni"' selon le nom exact du champ dans votre modèle User personnalisé
    diplomes = User.objects.filter(role='alumni')

    # ÉTAPE 2 : Récupération de toutes les filières existantes en base de données
    # Utilisé pour générer les options du menu déroulant de filtrage dans le formulaire HTML
    filieres = Filiere.objects.all()

    # ÉTAPE 3A : Lecture du paramètre de recherche textuelle depuis l'URL
    # request.GET.get('q', '') : retourne la valeur de ?q=... ou une chaîne vide si absent
    # .strip() : supprime les espaces parasites en début et fin de chaîne saisis par l'utilisateur
    recherche_nom = request.GET.get('q', '').strip()

    # ÉTAPE 3B : Lecture du paramètre de filtre par filière depuis l'URL
    # request.GET.get('filiere_id', '') : retourne la valeur de &filiere_id=... ou chaîne vide si absent
    # .strip() : nettoyage des espaces inutiles pour éviter des erreurs de comparaison
    filiere_selectionnee_id = request.GET.get('filiere_id', '').strip()

    # ÉTAPE 4 : Application conditionnelle du filtre textuel
    # Le bloc if s'exécute uniquement si l'utilisateur a saisi quelque chose dans la barre de recherche
    if recherche_nom:

        # Affinage du QuerySet 'diplomes' avec une condition OR multi-champs grâce à Q()
        # Sans Q(), Django ne permet que des conditions AND dans un seul .filter()
        diplomes = diplomes.filter(
            Q(first_name__icontains=recherche_nom) |    # Recherche dans le prénom (insensible à la casse)
            Q(last_name__icontains=recherche_nom)  |    # OU dans le nom de famille (insensible à la casse)
            Q(username__icontains=recherche_nom)        # OU dans le nom d'utilisateur (insensible à la casse)
            # __icontains : lookup Django équivalent à SQL LIKE '%valeur%' sans distinction majuscules/minuscules
            # Exemple : 'dupont' trouvera 'Dupont', 'DUPONT', 'dupont'
        )

    # ÉTAPE 5 : Application conditionnelle du filtre par filière
    # Le bloc if s'exécute uniquement si une filière a été sélectionnée dans le menu déroulant
    if filiere_selectionnee_id:

        # Affinage supplémentaire du QuerySet par clé étrangère
        # filiere_id : suffixe Django pour filtrer directement sur la clé primaire de la relation ForeignKey
        # Sans le suffixe _id, Django attendrait un objet Filiere complet au lieu d'un simple entier
        diplomes = diplomes.filter(filiere_id=filiere_selectionnee_id)
        #                          ^ Équivalent SQL : WHERE filiere_id = filiere_selectionnee_id

    # ÉTAPE 6 : Assemblage du dictionnaire de contexte transmis au template HTML
    context = {
        'diplomes': diplomes,                               # QuerySet filtré des anciens étudiants à afficher
        'filieres': filieres,                               # QuerySet de toutes les filières (menu déroulant)
        'recherche_nom': recherche_nom,                     # Valeur mémorisée pour la réafficher dans la barre de recherche
        'filiere_selectionnee_id': filiere_selectionnee_id, # ID mémorisé pour maintenir la filière active dans le menu
    }
    #  ^ Chaque clé du dictionnaire devient une variable directement accessible dans le template
    #    Exemple : {{ diplomes }}, {{ filieres }}, {{ recherche_nom }}, {{ filiere_selectionnee_id }}

    # Rendu final : Django compile le template HTML avec les données du contexte
    # et retourne une réponse HTTP complète envoyée au navigateur de l'utilisateur
    return render(request, 'alumni/alumni.html', context)
    #                       ^ Chemin relatif au dossier 'templates' de l'application alumni