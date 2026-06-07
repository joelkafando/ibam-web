# Importation du module models de Django pour définir les champs et le comportement du modèle
from django.db import models

# Importation du module timezone de Django pour la gestion des dates et heures
# Préférable à datetime.now() car timezone.now() respecte le fuseau horaire défini dans settings.py (USE_TZ = True)
from django.utils import timezone


# ==========================================
# MODÈLE : ANNONCE (ANNOUNCEMENT)
# ==========================================

# Définition du modèle Announcement qui hérite de models.Model (classe de base Django)
# Chaque instance de ce modèle correspond à une ligne dans la table 'announcements_announcement' en base de données
class Announcement(models.Model):
    """
    Modèle gérant la publication des annonces de l'établissement.
    Prend en charge le ciblage par catégorie, les pièces jointes et une date d'expiration.
    """

    # Liste de tuples définissant les catégories disponibles pour classifier une annonce
    # Format : ('code_stocké_en_BDD', 'Label affiché dans l'interface utilisateur')
    # Avantage : stocke un code court en base de données tout en affichant un label lisible
    CATEGORY_CHOICES = [
        ('ACAD', 'Académique'),     # Annonces liées aux cours, examens, résultats académiques
        ('ADMIN', 'Administratif'), # Annonces liées aux démarches administratives, inscriptions
        ('EVENT', 'Événement'),     # Annonces liées aux événements, conférences, sorties
    ]

    # Champ texte court pour le titre principal de l'annonce
    # max_length=200 : limite la longueur du titre à 200 caractères en base de données
    title = models.CharField(max_length=200)

    # Champ de sélection pour la catégorie de l'annonce
    # max_length=5 : longueur suffisante pour stocker les codes courts ('ACAD', 'ADMIN', 'EVENT')
    # choices=CATEGORY_CHOICES : restreint les valeurs à la liste définie ci-dessus (menu déroulant)
    # default='EVENT' : toute nouvelle annonce est classée 'Événement' si aucune catégorie n'est précisée
    category = models.CharField(
        max_length=5,
        choices=CATEGORY_CHOICES,   # Génère un menu déroulant dans les formulaires et l'interface admin
        default='EVENT'             # Valeur pré-sélectionnée à la création d'une nouvelle annonce
    )

    # Champ texte long (sans limite de caractères) pour le corps complet du message de l'annonce
    # TextField est adapté aux contenus longs contrairement à CharField qui a une limite obligatoire
    content = models.TextField()

    # Champ de téléversement d'image optionnel pour illustrer visuellement l'annonce
    # upload_to : sous-dossier dans MEDIA_ROOT où les images seront physiquement stockées sur le serveur
    # blank=True : champ non obligatoire dans les formulaires Django (validation côté Python)
    # null=True : autorise la valeur NULL en base de données si aucune image n'est fournie
    image = models.ImageField(
        upload_to='announcements/images/', # Chemin de stockage → media/announcements/images/
        blank=True,                        # Champ facultatif dans les formulaires
        null=True                          # NULL autorisé en base : une annonce peut ne pas avoir d'image
    )

    # Champ de téléversement de fichier optionnel pour joindre un document téléchargeable
    # upload_to : sous-dossier dédié aux documents joints dans MEDIA_ROOT
    # blank=True + null=True : pièce jointe entièrement facultative (même logique que le champ image)
    file = models.FileField(
        upload_to='announcements/docs/',   # Chemin de stockage → media/announcements/docs/
        blank=True,                        # Champ facultatif dans les formulaires
        null=True                          # NULL autorisé en base : une annonce peut ne pas avoir de fichier joint
    )

    # Champ date/heure pour l'horodatage de publication de l'annonce
    # default=timezone.now : la date est définie à l'heure courante au moment de la création
    # Différence avec auto_now_add=True : cette valeur est modifiable par l'administrateur si besoin
    # timezone.now : respecte le fuseau horaire défini dans settings.py (contrairement à datetime.now)
    date_published = models.DateTimeField(default=timezone.now)

    # Champ date/heure optionnel définissant la date limite de validité de l'annonce
    # null=True : une annonce sans date d'expiration restera visible indéfiniment
    # blank=True : champ non obligatoire dans les formulaires (peut être laissé vide)
    date_expiry = models.DateTimeField(
        null=True,  # NULL autorisé : l'annonce est valide indéfiniment si aucune date n'est définie
        blank=True  # Champ facultatif dans les formulaires de création et modification
    )

    # Champ booléen pour contrôler la visibilité de l'annonce sur le site
    # default=True : toute nouvelle annonce est visible immédiatement après publication
    # Permet de masquer instantanément une annonce sans la supprimer définitivement de la base de données
    is_active = models.BooleanField(default=True)
    #                                ^ True = annonce visible | False = annonce masquée sur le site

    # Classe interne Meta : configure les options globales de comportement du modèle
    class Meta:

        # Définit l'ordre de tri par défaut appliqué à toutes les requêtes sans .order_by() explicite
        # '-date_published' : le signe '-' indique un tri décroissant (plus récente en premier)
        # Résultat : les annonces les plus récentes apparaissent toujours en haut de la liste
        ordering = ['-date_published']
        #            ^ '-' = ordre décroissant | sans '-' ce serait ordre croissant (plus ancienne en premier)

    # Méthode spéciale Python définissant la représentation textuelle d'un objet Announcement
    # Utilisée dans l'interface admin, les logs et partout où l'objet est affiché comme texte
    def __str__(self):
        """
        Représentation textuelle de l'objet (affiche le titre dans le panneau d'administration).
        """
        # Retourne directement le titre de l'annonce
        # Exemple d'affichage dans l'admin : "Réunion pédagogique du 15 juin" au lieu de "Announcement object (1)"
        return self.title