from django.db import models
from django.utils import timezone

# ==========================================
# MODÈLE : ANNONCE (ANNOUNCEMENT)
# ==========================================
class Announcement(models.Model):
    """
    Modèle gérant la publication des annonces de l'établissement.
    Prend en charge le ciblage par catégorie, les pièces jointes et une date d'expiration.
    """
    
    # Options fixes pour classifier le type d'annonce (Code stocké, Label affiché)
    CATEGORY_CHOICES = [
        ('ACAD', 'Académique'),
        ('ADMIN', 'Administratif'),
        ('EVENT', 'Événement'),
    ]

    # Titre principal de la publication
    title = models.CharField(max_length=200)
    
    # Menu déroulant basé sur CATEGORY_CHOICES (Catégorie 'Événement' affectée par défaut)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default='EVENT')
    
    # Corps ou texte détaillé du message de l'annonce
    content = models.TextField()
    
    # Illustration visuelle optionnelle (enregistrée dans le sous-dossier spécifié de MEDIA_ROOT)
    image = models.ImageField(upload_to='announcements/images/', blank=True, null=True)
    
    # Document téléchargeable ou pièce jointe optionnelle (PDF, Word, etc.)
    file = models.FileField(upload_to='announcements/docs/', blank=True, null=True)
    
    # Horodatage de la publication (initialisé automatiquement à la date et heure courantes)
    date_published = models.DateTimeField(default=timezone.now)
    
    # Date limite optionnelle après laquelle l'annonce n'est plus pertinente
    date_expiry = models.DateTimeField(null=True, blank=True)
    
    # Case à cocher pour afficher ou masquer instantanément l'annonce sur le site
    is_active = models.BooleanField(default=True)

    # Options de configuration et de comportement du modèle
    class Meta:
        # Tri automatique par défaut : de la publication la plus récente à la plus ancienne
        ordering = ['-date_published']

    def __str__(self):
        """
        Représentation textuelle de l'objet (affiche le titre dans le panneau d'administration).
        """
        return self.title
