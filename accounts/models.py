from django.contrib.auth.models import AbstractUser
from django.db import models
from academics.models import Filiere

# ==========================================
# MODÈLE UTILISATEUR PERSONNALISÉ (CUSTOM USER)
# ==========================================
class Utilisateur(AbstractUser):
    # Liste des rôles disponibles pour segmenter les profils utilisateurs
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
       # ('ENSEIGNANT', 'Enseignant'),
        ('ETUDIANT', 'Étudiant'),
        ('ALUMNI', 'Alumni'),
    ]
    
    # Première définition du champ filiere (avec verbose_name personnalisé)
    filiere = models.ForeignKey(
        Filiere, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='utilisateurs',
        verbose_name="Filière (Étudiants/Alumni)"
    )
    
    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode de sauvegarde pour automatiser des règles métiers.
        """
        # Automatisation : Si c'est un superutilisateur, son rôle devient ADMIN d'office
        if self.is_superuser:
            self.role_user = 'ADMIN'
        # Exécution de la sauvegarde parente native de Django
        super().save(*args, **kwargs)

    # Champ de sélection du rôle applicatif (Étudiant par défaut)
    role_user = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ETUDIANT')
    
    # Seconde définition du champ filiere (avec les options de base)
    # Un étudiant ou un alumni appartient à une filière (optionnel pour les admins/enseignants)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs')

    def __str__(self):
        """
        Représentation textuelle affichant l'identifiant et le libellé du rôle.
        """
        return f"{self.username} ({self.get_role_user_display()})"

   