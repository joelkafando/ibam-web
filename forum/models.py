from django.db import models
from django.conf import settings

# ==========================================
# 1. MODÈLE : CATÉGORIE DU FORUM
# ==========================================
class CategorieForum(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.CharField(max_length=250, verbose_name="Description rapide")
    icone = models.CharField(max_length=50, default="fas fa-comments", help_text="Classe FontAwesome (ex: fas fa-graduation-cap)")

    class Meta:
        verbose_name = "Catégorie Forum"
        verbose_name_plural = "Catégories Forum"

    def __str__(self):
        return self.nom


# ==========================================
# 2. MODÈLE : SUJET DE DISCUSSION (TOPIC)
# ==========================================
class SujetForum(models.Model):
    categorie = models.ForeignKey(CategorieForum, on_delete=models.CASCADE, related_name='sujets')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sujets_forum')
    titre = models.CharField(max_length=200, verbose_name="Titre du sujet")
    message_origine = models.TextField(verbose_name="Message initial")
    date_creation = models.DateTimeField(auto_now_add=True)
    est_epinglé = models.BooleanField(default=False, verbose_name="Épingler en haut")

    class Meta:
        verbose_name = "Sujet de discussion"
        verbose_name_plural = "Sujets de discussion"
        ordering = ['-est_epinglé', '-date_creation']

    def __str__(self):
        return self.titre


# ==========================================
# 3. MODÈLE : RÉPONSE / COMMENTAIRE
# ==========================================
class ReponseForum(models.Model):
    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE, related_name='reponses')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reponses_forum')
    contenu = models.TextField(verbose_name="Votre réponse")
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        ordering = ['date_publication']

    def __str__(self):
        return f"Réponse de {self.auteur.username} sur '{self.sujet.titre}'"
