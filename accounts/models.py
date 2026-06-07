# Importation de AbstractUser : classe de base Django qui fournit tous les champs
# et comportements standards d'un utilisateur (username, password, email, is_staff, etc.)
# On en hérite pour étendre le modèle User sans repartir de zéro
from django.contrib.auth.models import AbstractUser

# Importation du module models de Django pour définir les champs personnalisés
from django.db import models

# Importation du modèle Filiere depuis l'application academics
# Permet de lier chaque utilisateur à une formation existante via une clé étrangère
from academics.models import Filiere


# Définition du modèle Utilisateur personnalisé qui hérite de AbstractUser
# AbstractUser fournit déjà : username, password, email, first_name, last_name,
# is_staff, is_active, is_superuser, date_joined, last_login, groups, permissions
class Utilisateur(AbstractUser):

    # Liste de tuples définissant les rôles possibles dans le système
    # Format : ('valeur_stockée_en_BDD', 'Label affiché dans l'interface')
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),    # Accès complet à toutes les fonctionnalités
        ('ENSEIGNANT', 'Enseignant'),   # Accès à la gestion des cours et ressources
        ('ETUDIANT', 'Étudiant'),       # Accès à la consultation de l'emploi du temps et des ressources
        ('ALUMNI', 'Alumni'),           # Accès à l'annuaire et aux fonctionnalités anciens élèves
    ]

    # Liste de tuples définissant les niveaux d'études disponibles
    # Réutilisée dans d'autres parties du projet (forms.py, academics/models.py)
    CHOICES_NIVEAU = [
        ('Licence 1', 'Licence 1'),     # Première année de Licence
        ('Licence 2', 'Licence 2'),     # Deuxième année de Licence
        ('Licence 3', 'Licence 3'),     # Troisième année de Licence
        ('Master 1', 'Master 1'),       # Première année de Master
        ('Master 2', 'Master 2'),       # Deuxième année de Master
    ]

    # Champ de sélection pour le rôle de l'utilisateur dans le système
    # max_length=20 : longueur suffisante pour stocker les codes comme 'ENSEIGNANT'
    # choices=ROLE_CHOICES : restreint les valeurs possibles à la liste définie ci-dessus
    # default='ETUDIANT' : tout nouvel utilisateur est créé avec le rôle étudiant par défaut
    # verbose_name : label affiché dans l'interface d'administration Django
    role_user = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='ETUDIANT',         # Valeur attribuée automatiquement si aucun rôle n'est précisé
        verbose_name="Rôle"         # Label affiché dans l'admin et les formulaires ModelForm
    )

    # Clé étrangère vers le modèle Filiere de l'application academics
    # on_delete=SET_NULL : si la filière est supprimée, le champ devient NULL (l'utilisateur est conservé)
    # null=True : autorise la valeur NULL en base de données (champ non obligatoire côté SQL)
    # blank=True : autorise le champ vide dans les formulaires Django (validation côté Python)
    # related_name : permet d'accéder aux utilisateurs depuis une filière → filiere.utilisateurs.all()
    # verbose_name : label affiché dans l'interface d'administration
    filiere = models.ForeignKey(
        Filiere,                        # Référence directe au modèle Filiere importé en haut du fichier
        on_delete=models.SET_NULL,      # Comportement à la suppression : met le champ à NULL (pas de cascade)
        null=True,                      # NULL autorisé en base : un utilisateur peut n'avoir aucune filière
        blank=True,                     # Champ facultatif dans les formulaires : non obligatoire à la saisie
        related_name='utilisateurs',    # Nom du lien inverse pour accéder aux utilisateurs depuis Filiere
        verbose_name="Filière"          # Label affiché dans l'interface d'administration Django
    )

    # Champ de sélection pour le niveau d'études de l'utilisateur
    # Utilisé principalement pour les étudiants afin de filtrer leurs cours et ressources
    # max_length=20 : longueur suffisante pour 'Licence 1' à 'Master 2'
    # choices=CHOICES_NIVEAU : restreint les valeurs possibles à la liste définie plus haut
    # null=True : NULL autorisé (les enseignants et admins n'ont pas de niveau d'études)
    # blank=True : champ facultatif dans les formulaires (non obligatoire pour tous les rôles)
    # verbose_name : label explicite précisant que ce champ concerne principalement les étudiants
    niveau_etude = models.CharField(
        max_length=20,
        choices=CHOICES_NIVEAU,
        null=True,                                          # Autorise NULL : les admins et enseignants n'ont pas de niveau
        blank=True,                                         # Champ non obligatoire dans les formulaires
        verbose_name="Niveau d'études (Étudiants)"          # Label indiquant que ce champ est dédié aux étudiants
    )

    # Surcharge de la méthode save() pour ajouter une logique automatique avant chaque sauvegarde
    # *args et **kwargs : capture tous les arguments positionnels et nommés transmis par Django
    # (nécessaire pour ne pas casser la signature de la méthode parente)
    def save(self, *args, **kwargs):

        # Vérification du statut superutilisateur avant toute sauvegarde
        # Si l'utilisateur est superuser, son rôle est automatiquement forcé à 'ADMIN'
        # Empêche qu'un superutilisateur ait un rôle incohérent (ex: 'ETUDIANT')
        if self.is_superuser:
            self.role_user = 'ADMIN'    # Forçage automatique du rôle ADMIN pour tout superutilisateur

        # Appel de la méthode save() de la classe parente (AbstractUser)
        # Indispensable : sans ce super().save(), l'objet ne serait jamais écrit en base de données
        # *args, **kwargs : retransmission de tous les arguments reçus pour respecter le comportement natif
        super().save(*args, **kwargs)

    # Méthode spéciale Python définissant la représentation textuelle d'un objet Utilisateur
    # Utilisée dans l'interface admin, les logs, et partout où l'objet est affiché comme texte
    def __str__(self):
        # get_role_user_display() : méthode auto-générée par Django pour les champs 'choices'
        # Retourne le label lisible du rôle au lieu du code stocké en base
        # Exemple : 'ENSEIGNANT' → 'Enseignant' | 'ETUDIANT' → 'Étudiant'
        # Résultat final : ex → "prof_martin (Enseignant)" ou "etudiant_dupont (Étudiant)"
        return f"{self.username} ({self.get_role_user_display()})"