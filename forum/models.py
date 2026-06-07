# Importation du module models de Django pour définir les modèles de base de données
from django.db import models

# Importation de settings pour référencer le modèle utilisateur de manière flexible
# Permet de supporter un modèle User personnalisé sans coder "auth.User" en dur
from django.conf import settings


# ==========================================
# 1. MODÈLE : CATÉGORIE DU FORUM
# ==========================================

class CategorieForum(models.Model):

    # Champ texte court pour le nom de la catégorie (ex: "Vie étudiante", "Cours")
    # max_length=100 : limite à 100 caractères maximum
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

    # Champ texte court pour une description synthétique de la catégorie
    # verbose_name : libellé affiché dans l'interface d'administration Django
    description = models.CharField(max_length=250, verbose_name="Description rapide")

    # Champ texte pour stocker la classe CSS FontAwesome de l'icône associée
    # default : valeur appliquée automatiquement si aucune icône n'est renseignée
    # help_text : texte d'aide affiché dans le formulaire d'administration
    icone = models.CharField(
        max_length=50,
        default="fas fa-comments",
        help_text="Classe FontAwesome (ex: fas fa-graduation-cap)"
    )

    # Classe interne Meta : configure les métadonnées du modèle pour Django
    class Meta:
        # Nom singulier affiché dans l'interface d'administration Django
        verbose_name = "Catégorie Forum"

        # Nom pluriel affiché dans l'interface d'administration Django
        verbose_name_plural = "Catégories Forum"

    # Méthode de représentation textuelle de l'objet
    # Utilisée dans l'admin Django et dans les menus déroulants des formulaires
    def __str__(self):
        # Retourne le nom de la catégorie comme représentation lisible
        return self.nom


# ==========================================
# 2. MODÈLE : SUJET DE DISCUSSION (TOPIC)
# ==========================================

class SujetForum(models.Model):

    # Clé étrangère vers CategorieForum : chaque sujet appartient à une catégorie
    # on_delete=CASCADE : si la catégorie est supprimée, tous ses sujets le sont aussi
    # related_name='sujets' : permet d'accéder aux sujets depuis une catégorie via categorie.sujets.all()
    categorie = models.ForeignKey(
        CategorieForum,
        on_delete=models.CASCADE,
        related_name='sujets'
    )

    # Clé étrangère vers le modèle utilisateur actif du projet
    # settings.AUTH_USER_MODEL : référence flexible qui supporte un User personnalisé
    # on_delete=CASCADE : si l'auteur est supprimé, ses sujets le sont aussi
    # related_name='sujets_forum' : accès aux sujets d'un utilisateur via user.sujets_forum.all()
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sujets_forum'
    )

    # Champ texte court pour le titre du sujet de discussion
    titre = models.CharField(max_length=200, verbose_name="Titre du sujet")

    # Champ texte long (sans limite de caractères) pour le message d'ouverture du sujet
    message_origine = models.TextField(verbose_name="Message initial")

    # Date et heure de création du sujet, renseignées automatiquement à la création
    # auto_now_add=True : valeur définie une seule fois à la création, jamais modifiée
    date_creation = models.DateTimeField(auto_now_add=True)

    # Champ booléen pour épingler un sujet en haut de la liste
    # default=False : par défaut, aucun sujet n'est épinglé
    est_epinglé = models.BooleanField(default=False, verbose_name="Épingler en haut")

    # Classe interne Meta : configure les métadonnées et le tri par défaut
    class Meta:
        # Nom singulier affiché dans l'interface d'administration
        verbose_name = "Sujet de discussion"

        # Nom pluriel affiché dans l'interface d'administration
        verbose_name_plural = "Sujets de discussion"

        # Tri par défaut des sujets : épinglés en premier, puis du plus récent au plus ancien
        # Le signe "-" devant le nom du champ signifie un tri décroissant
        ordering = ['-est_epinglé', '-date_creation']

    # Représentation textuelle du sujet (affiché dans l'admin et les logs)
    def __str__(self):
        # Retourne le titre du sujet comme représentation lisible
        return self.titre


# ==========================================
# 3. MODÈLE : RÉPONSE / COMMENTAIRE
# ==========================================

class ReponseForum(models.Model):

    # Clé étrangère vers SujetForum : chaque réponse est rattachée à un sujet
    # on_delete=CASCADE : si le sujet est supprimé, toutes ses réponses le sont aussi
    # related_name='reponses' : accès aux réponses depuis un sujet via sujet.reponses.all()
    sujet = models.ForeignKey(
        SujetForum,
        on_delete=models.CASCADE,
        related_name='reponses'
    )

    # Clé étrangère vers le modèle utilisateur : l'auteur de la réponse
    # on_delete=CASCADE : si l'utilisateur est supprimé, ses réponses le sont aussi
    # related_name='reponses_forum' : accès aux réponses d'un utilisateur via user.reponses_forum.all()
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reponses_forum'
    )

    # Champ texte long pour le contenu de la réponse (sans limite de caractères)
    contenu = models.TextField(verbose_name="Votre réponse")

    # Date et heure de publication de la réponse, enregistrées automatiquement à la création
    # auto_now_add=True : valeur figée à la création, jamais mise à jour ensuite
    date_publication = models.DateTimeField(auto_now_add=True)

    # Classe interne Meta : configure les métadonnées et le tri par défaut
    class Meta:
        # Nom singulier affiché dans l'interface d'administration
        verbose_name = "Réponse"

        # Nom pluriel affiché dans l'interface d'administration
        verbose_name_plural = "Réponses"

        # Tri chronologique croissant : les réponses s'affichent de la plus ancienne à la plus récente
        # (pas de "-" devant date_publication = ordre croissant)
        ordering = ['date_publication']

    # Représentation textuelle de la réponse (utile dans l'admin et les logs)
    def __str__(self):
        # Retourne une phrase descriptive combinant l'auteur et le titre du sujet concerné
        return f"Réponse de {self.auteur.username} sur '{self.sujet.titre}'"