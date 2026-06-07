# Importation du module admin de Django pour accéder à l'interface d'administration
from django.contrib import admin

# Importation de UserAdmin : classe d'administration par défaut de Django pour le modèle User
# Elle fournit tous les formulaires, sections et comportements standards de gestion des utilisateurs
# On en hérite pour ne pas repartir de zéro et juste étendre ses fonctionnalités
from django.contrib.auth.admin import UserAdmin

# Importation du modèle Utilisateur personnalisé depuis le fichier models.py de l'application courante
from .models import Utilisateur


# Définition de la classe d'administration personnalisée pour le modèle Utilisateur
# Elle hérite de UserAdmin pour conserver toutes les fonctionnalités natives (mot de passe, permissions...)
# et y ajouter les champs métier spécifiques à l'établissement (rôle, filière, niveau)
class UtilisateurAdmin(UserAdmin):

    # 1. Définition des colonnes affichées dans le tableau récapitulatif de la liste des utilisateurs
    #    Chaque chaîne correspond à un champ du modèle Utilisateur ou de son parent AbstractUser
    list_display = (
        'username',      # Nom d'utilisateur (identifiant de connexion)
        'email',         # Adresse email de l'utilisateur
        'last_name',     # Nom de famille (hérité de AbstractUser)
        'first_name',    # Prénom (hérité de AbstractUser)
        'role_user',     # Rôle personnalisé dans l'établissement (ex: ETUDIANT, ENSEIGNANT, ALUMNI)
        'filiere',       # Filière d'appartenance (champ personnalisé ajouté au modèle)
        'niveau_etude',  # Niveau d'études de l'utilisateur (ex: Licence 1, Master 2)
        'is_staff'       # Booléen indiquant si l'utilisateur a accès à l'interface d'administration
    )

    # 2. Définition des filtres latéraux affichés dans le panneau de droite de la liste
    #    Permet de filtrer rapidement les utilisateurs selon ces critères d'un simple clic
    list_filter = (
        'role_user',     # Filtre par rôle : affiche uniquement les ENSEIGNANTS, ETUDIANTS, etc.
        'filiere',       # Filtre par filière : affiche uniquement les utilisateurs d'une filière
        'niveau_etude',  # Filtre par niveau d'étude : affiche uniquement un niveau précis
        'is_staff',      # Filtre par statut staff : sépare les admins des utilisateurs normaux
        'is_superuser'   # Filtre par statut superutilisateur : isole les comptes à tous les droits
    )

    # 3. Configuration du formulaire de MODIFICATION d'un utilisateur existant dans l'admin
    #    UserAdmin.fieldsets : récupère TOUTES les sections natives de Django (Infos perso, Permissions...)
    #    L'opérateur + : concatène un tuple supplémentaire contenant notre section personnalisée
    #    Sans ce + , les champs natifs (mot de passe, permissions) disparaîtraient du formulaire
    fieldsets = UserAdmin.fieldsets + (

        # Nouvelle section ajoutée à la suite des sections natives de UserAdmin
        # 'Informations Institutionnelles IBAM' : titre affiché dans l'encadré de la section
        ('Informations Institutionnelles IBAM', {

            # 'fields' : liste des champs personnalisés à afficher dans cette section
            'fields': ('role_user', 'filiere', 'niveau_etude'),
            #           ^ Rôle IBAM  ^ Filière     ^ Niveau d'étude
        }),
    )
    # Note : la virgule après }) est obligatoire pour que Python reconnaisse un tuple à un seul élément

    # 4. Configuration du formulaire de CRÉATION d'un nouvel utilisateur directement dans l'admin
    #    UserAdmin.add_fieldsets : récupère les champs natifs du formulaire de création (username, password...)
    #    L'opérateur + : y ajoute notre section de champs institutionnels personnalisés
    #    Sans ce + , il serait impossible de renseigner le rôle ou la filière à la création du compte
    add_fieldsets = UserAdmin.add_fieldsets + (

        # Section identique à celle du formulaire de modification, mais pour le formulaire de création
        ('Informations Institutionnelles IBAM', {

            # Mêmes champs personnalisés disponibles dès la création du compte utilisateur
            'fields': ('role_user', 'filiere', 'niveau_etude'),
            #           ^ Rôle IBAM  ^ Filière     ^ Niveau d'étude
        }),
    )
    # Note : la virgule finale est à nouveau obligatoire pour maintenir la structure en tuple


# Enregistrement UNIQUE du modèle Utilisateur dans l'interface d'administration Django
# Paramètre 1 : le modèle à enregistrer (Utilisateur)
# Paramètre 2 : la classe d'administration personnalisée qui définit son comportement (UtilisateurAdmin)
# ATTENTION : un double enregistrement du même modèle lèverait une AlreadyRegistered exception au démarrage
admin.site.register(Utilisateur, UtilisateurAdmin)